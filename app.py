# app.py
import time
import hashlib
import json
import mysql
import requests
import os
import logging
from datetime import datetime, date, timedelta, timezone
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date, timedelta
from schedule import logger
from werkzeug.security import generate_password_hash, check_password_hash
from multiprocessing import Process
# lokal modules (asumsi sudah ada)
import config
from pipeline.scraper import translate_to_indonesian
from pipeline import bot_id, mysql_connector as db
from pipeline.scraper import scrape_latest_review, parse_review_time
from pipeline.model_predict import ModelPredict
from pipeline.pipeline import run_pipeline 
from pipeline import mysql_connector #import get_latest_sentiment, get_weekly_comparison, get_review_stats, get_rating_distribution, get_average_rating
# coba downlod
import csv
import io
import pandas as pd  
from flask import Response, request 
from pipeline import mysql_connector as db
# coba boot controler
from flask_login import login_required
from pipeline.bot_controller import start_bot, stop_bot, bot_status
from pipeline.bot_controller import bot_bp

app = Flask(__name__)
app.register_blueprint(bot_bp)
app.secret_key = config.SECRET_KEY or os.urandom(32)
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()
JOB_ID = "scrape_job_single"
MODEL = ModelPredict()  # inisialisasi model
# gunakan file-based timestamp agar shared antar-process (fallback jika tidak ada external store)
TIMESTAMP_FILE = os.path.join(config.DATA_DIR if hasattr(config, "DATA_DIR") else ".", ".last_scrape_ts")
MIN_SCRAPE_INTERVAL = getattr(config, "MIN_SCRAPE_INTERVAL_SEC", 30)
# Bot process container
bot_process = None


# Helpers 
def md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()

def _read_last_ts():
    try:
        with open(TIMESTAMP_FILE, "r") as f:
            return float(f.read().strip() or "0")
    except Exception:
        return 0.0

def _write_last_ts(ts: float):
    # write atomically
    tmp = TIMESTAMP_FILE + ".tmp"
    with open(tmp, "w") as f:
        f.write(str(ts))
    os.replace(tmp, TIMESTAMP_FILE)

# Auth decorator (API vs Page aware) 
from functools import wraps
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "uid" not in session:
            # detect API call by path or Accept header or explicit JSON
            is_api = request.path.startswith("/api/") or request.path.startswith("/bot/") or request.is_json or request.headers.get("Accept","").startswith("application/json")
            if is_api:
                return jsonify({"ok": False, "msg": "Unauthorized"}), 401
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# Sentiment classification (benar) 
def classify_text_or_rating(text, rating):
    """
    Return (nb_label, svm_label, db_label)
    db_label normalized to ('Positive','Negative')
    - If text exists, use models
    - Else infer from rating: rating >=4 => Positive else Negative
    """
    def norm(lbl):
        if not lbl:
            return None
        s = (lbl or "").strip().lower()
        # menangani label bahasa indonesia / english
        if "positif" in s or "positive" in s or s == "pos" or s == "p":
            return "POSITIF"
        if "negatif" in s or "negative" in s or s == "neg" or s == "n":
            return "NEGATIF"
        return None

    if text and text.strip():
        try:
            nb = MODEL.predict_nb(text)
        except Exception:
            nb = None
        try:
            svm = MODEL.predict_svm(text)
        except Exception:
            svm = None

        db_label = norm(nb) or norm(svm) or "NEGATIF"
        # normalize returned labels to readable form
        nb = nb or "Unknown"
        svm = svm or "Unknown"
        return nb, svm, db_label
    else:
        rule = "POSITIF" if (int(rating or 0) >= 3) else "NEGATIF"
        # return nb, svm, db_label (both models absent so we duplicate rule)
        return rule, rule, rule

# Broadcast Telegram 
def broadcast_to_subscribers(saved_review):
    subs = db.get_subscribers()
    if not subs or not getattr(config, "TELEGRAM_BOT_TOKEN", None):
        return {"sent": 0, "failed": 0}
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    sent = failed = 0
    message = (
        "📢 <b>Review Baru</b>\n"
        f"👤 <b>User:</b> {saved_review.get('user_name')}\n"
        f"⭐ <b>Rating:</b> {saved_review.get('rating')}\n\n"
        f"📝 <b>Review:</b> {(saved_review.get('review_text') or '(None)')[:400]}\n\n"
        f"🤖 <b>Naive Bayes:</b> {saved_review.get('sentiment_nb')}\n"
        f"⚡ <b>SVM:</b> {saved_review.get('sentiment_svm')}\n\n"
        f"🕒 <b>Waktu:</b> {saved_review.get('review_time').strftime('%d/%m/%Y %H:%M:%S')}"
    )
    # safety: cap to telegram limit
    if len(message) > 3800:
        message = message[:3790] + "\n\n...(truncated)"

    for s in subs:
        payload = {"chat_id": s["chat_id"], "text": message, "parse_mode": "HTML"}
        try:
            r = requests.post(url, data=payload, timeout=12)
            ok = (r.status_code == 200 and r.json().get("ok", False))
        except Exception:
            ok = False
        status = "sent" if ok else "failed"
        try:
            db.log_notification(saved_review["review_id"], s["chat_id"], status)
        except Exception:
            pass
        if ok:
            sent += 1
        else:
            failed += 1
    return {"sent": sent, "failed": failed}

# Orchestration: one scrape run
def run_scrape_once():
    """
    1) call pipeline.scraper.scrape_latest_review, Ambil review terbaru dari Google Maps
    2) if you found the same review as last time, skip
    3) if found, save to hotel_reviews (raw) & sentiment_reviews
    4) broadcast to telegram & log notifications
    Returns dict with summary
    """
    try:
        reviews = scrape_latest_review(config.GOOGLE_DATA_ID, config.SERPAPI_KEY)
    except Exception as e:
        return {"ok": False, "msg": f"Scraper error: {e}"}

    if not reviews:
        return {"ok": True, "new": False, "msg": "No reviews"}

    r = reviews[0]

    # Normalisasi Teks
    text = r.get("text") or r.get("snippet")
    if text is not None:
        text = text.strip() or None  #Kosong jadi None
    
    # Rating
    try:
        rating = int(r.get("rating") or 0)
    except Exception:
        rating = 0
    # User
    user = r.get("user")
    user_name = (user.get("name") if isinstance(user, dict) else (user or "Unknown"))
    # Sumber dan Waktu
    source = r.get("source", "Google Maps")
    
    # Waktu review asli
    review_time = parse_review_time(r.get("time")) or datetime.now()

    # cek duplikat
    try:
        if db.review_exists(config.HOTEL_ID, user_name, text, rating, source):
            return {"ok": True, "new": False, "msg": "Review already exists, skipped"}
    except Exception as e:
        # jika fungsi db error, log dan lanjutkan (atau return error)
        return {"ok": False, "msg": f"DB error on review_exists: {e}"}

    # save raw review/ simpan ulasan mentah
    try:
        review_id = db.save_hotel_review(config.HOTEL_ID, user_name, text, rating, review_time, source)
    except Exception as e:
        return {"ok": False, "msg": f"DB error on save_hotel_review: {e}"}

    # classify
    nb, svm, db_label = classify_text_or_rating(text, rating)

    # save sentiment result
    try:
        sid = db.save_sentiment_review(
            review_id, config.HOTEL_ID, user_name, text, rating,
            review_time, nb, svm, source
        )
    except Exception as e:
        return {"ok": False, "msg": f"DB error on save_sentiment_review: {e}"}

    saved = {
        "review_id": review_id,
        "sentiment_id": sid,
        "user_name": user_name,
        "review_text": text,
        "rating": rating,
        "sentiment_nb": nb,
        "sentiment_svm": svm,
        "review_time": review_time, # waktu asli dari Google Maps
        "source": source
    }

    # broadcast
    stats = broadcast_to_subscribers(saved) if getattr(config, "TELEGRAM_BOT_TOKEN", None) else {"sent": 0, "failed": 0}
    return {"ok": True, "new": True, "saved": saved, "notify": stats}

# Scheduler and Scheduler control 
def scheduled_scrape_job():
    try:
        result = run_scrape_once()
        logger.info(f"Scheduled scrape executed: {result}")
    except Exception as e:
        logger.error(f"Scheduled scrape failed: {e}", exc_info=True)

# Routes & endpoints
@app.get("/login")
def login():
    if "uid" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.post("/login")
def login_post():
    username = request.form.get("username","").strip()
    password = request.form.get("password","")
    user = db.get_user_by_username(username)
    if not user or not check_password_hash(user["password"], password):
        return render_template("login.html", error="Username atau password salah")
    session["uid"] = user["user_id"]
    session["uname"] = user["username"]
    # guard: if user is not dict-like with .get
    role = user.get("role") if isinstance(user, dict) else getattr(user, "role", "user")
    session["role"] = role or "user"
    return redirect(url_for("dashboard"))

@app.get("/register")
def register():
    return render_template("register.html")

@app.post("/register")
def register_post():
    username = request.form.get("username","").strip()
    password = request.form.get("password","")
    if not username or not password:
        return redirect(url_for("register"))
    if db.get_user_by_username(username):
        return redirect(url_for("register"))
    pw_hash = generate_password_hash(password)
    db.create_user(username, pw_hash, role="user")
    return redirect(url_for("login"))

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Lupa Password & Ganti Password 
@app.get("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")

@app.post("/forgot-password")
def forgot_password_post():
    username = request.form.get("username", "").strip()
    user = db.get_user_by_username(username)
    if not user:
        return render_template("forgot_password.html", message="Username tidak ditemukan")

    # Nanti di sini bisa kirim email reset link, tapi untuk demo langsung redirect
    return redirect(url_for("reset_password", username=username))

@app.get("/reset-password/<username>")
def reset_password(username):
    user = db.get_user_by_username(username)
    if not user:
        return redirect(url_for("forgot_password"))
    return render_template("reset_password.html", username=username)

@app.post("/reset-password/<username>")
def reset_password_post(username):
    new_password = request.form.get("new_password", "")
    if not new_password:
        return render_template("reset_password.html", error="Password tidak boleh kosong", username=username)

    pw_hash = generate_password_hash(new_password)
    db.update_user_password(username, pw_hash)
    return redirect(url_for("login"))
# End Lupa Password & Ganti Password 

@app.get("/")
@login_required
def index():
    return redirect(url_for("dashboard"))

# dashboard
@app.get("/dashboard")
@login_required
def dashboard():
    # Ambil data utama dari database
    hotel = db.get_hotel(config.HOTEL_ID)
    latest = db.get_latest_reviews(config.HOTEL_ID, limit=1)  # Review terbaru
    counts = db.count_sentiments(config.HOTEL_ID)
    trend = db.trend_reviews(config.HOTEL_ID, days=7)
    total_reviews = db.get_review_stats(config.HOTEL_ID)
    diff_reviews = counts.get("POSITIF", 0) - counts.get("NEGATIF", 0)
    weekly = db.get_weekly_comparison(config.HOTEL_ID)
    
    # Tambahan: data rating
    avg_rating = db.get_average_rating(config.HOTEL_ID)
    count_by_star = db.get_rating_distribution(config.HOTEL_ID)  # misal return dict {5:10,4:4,3:2,...}

    # Perhitungan distribusi rating agar total = 100% 
    rating_dist = {}
    total_count = sum(count_by_star.values()) or 1  # hindari div by zero
    # Hitung persentase mentah
    raw_percentages = {
        star: (count_by_star.get(star, 0) / total_count) * 100
        for star in range(1, 6)
    }

    # Bulatkan & hitung total
    rating_dist = {star: round(raw_percentages[star]) for star in raw_percentages}
    total_rounded = sum(rating_dist.values())

    # Koreksi selisih (agar total tepat 100%)
    diff = 100 - total_rounded
    if diff != 0:
        # Tambahkan/kurangi ke bintang 5 (atau rating tertinggi yang punya nilai)
        for star in range(5, 0, -1):
            if rating_dist.get(star, 0) + diff >= 0:
                rating_dist[star] += diff
                break

    # 🔹 Keyword analytics
    keywords = db.get_top_keywords(config.HOTEL_ID, limit=5)

    # Kirim semua data ke template
    return render_template(
        "dashboard.html",
        hotel=hotel,
        avg_rating=avg_rating,
        rating_dist=rating_dist,
        latest=latest,
        trend=trend,
        counts=counts,
        total_reviews=total_reviews,
        diff_reviews=diff_reviews,
        keywords=keywords,
        weekly=weekly
    )

# Halaman review
@app.get("/reviews")
@login_required
def reviews_page():
    rows = db.list_sentiments(config.HOTEL_ID, limit=1000)
    return render_template("reviews.html", rows=rows)

# Route untuk halaman review
@app.get("/reviews")
@login_required
def reviews():
    conn = db.get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT review_date, user_name, rating, review_text, sentiment_nb, sentiment_svm 
        FROM sentiment_reviews 
        ORDER BY review_date DESC 
        LIMIT 200
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return render_template("reviews.html", rows=rows)

#  Route untuk Export Reviews
@app.get("/reviews/export/<fmt>")
@login_required
def export_reviews(fmt):
    limit = request.args.get("limit", type=int)
    sentiment = request.args.get("filter", "all")
    rating = request.args.get("rating", "all")
    model = request.args.get("model", "all")
    date_filter = request.args.get("date", "all")
    start = request.args.get("start")
    end = request.args.get("end")
    query = """
        SELECT review_date, user_name, rating, review_text, sentiment_nb, sentiment_svm
        FROM sentiment_reviews
        WHERE 1=1
    """
    params = []
    # Filter sentiment umum (Naive Bayes default)
    if sentiment in ("positif", "negatif"):
        query += " AND sentiment_nb = %s"
        params.append(sentiment.upper())
    # Filter rating
    if rating.isdigit():
        query += " AND rating = %s"
        params.append(int(rating))
    # Filter model
    if model == "nb_pos":
        query += " AND sentiment_nb = 'POSITIF'"
    elif model == "nb_neg":
        query += " AND sentiment_nb = 'NEGATIF'"
    elif model == "svm_pos":
        query += " AND sentiment_svm = 'POSITIF'"
    elif model == "svm_neg":
        query += " AND sentiment_svm = 'NEGATIF'"
    # Filter tanggal (pakai MySQL DATE_FORMAT / BETWEEN)
    if date_filter == "month":
        now = datetime.now().strftime("%Y-%m")
        query += " AND DATE_FORMAT(review_date, '%%Y-%%m') = %s"
        params.append(now)
    elif date_filter == "range" and start and end:
        query += " AND DATE(review_date) BETWEEN %s AND %s"
        params.extend([start, end])
    query += " ORDER BY review_date DESC"
    if limit:
        query += f" LIMIT {limit}"

    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    cur.close(); conn.close()

    # Export CSV
    if fmt == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Tanggal", "User", "Rating", "Text", "Naive Bayes", "SVM"])
        for r in rows:
            writer.writerow(r)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=reviews.csv"}
        )

    # Export XLS 
    elif fmt in ("xls", "xlsx"):
        df = pd.DataFrame(rows, columns=["Tanggal", "User", "Rating", "Text", "Naive Bayes", "SVM"])
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return Response(
            output.read(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment;filename=reviews.xlsx"}
        )
    return jsonify({"ok": False, "msg": "Format not supported"})

#Halaman subcriber
@app.get("/subscribers")
@login_required
def subscribers_page():
    subs = db.get_subscribers()
    return render_template("subscribers.html", subs=subs)

@app.post("/subscribers")
@login_required
def subscribers_add():
    chat_id = request.form.get("chat_id")
    if chat_id:
        try:
            db.add_subscriber(int(chat_id))
        except Exception:
            pass
    return redirect(url_for("subscribers_page"))

#Halaman notifications
@app.get("/notifications")
@login_required
def notifications_page():
    rows = db.get_notifications(limit=500)
    return render_template("notifications.html", rows=rows)
# coba scearch 
@app.route('/api/notifications')
def get_notifications():
    limit = request.args.get('limit', default=150, type=int)
    if limit == 0:
        rows = db.get_notifications(limit=None)
    else:
        rows = db.get_notifications(limit=limit)
    return jsonify(rows)

# Halaman analytic
@app.get("/analytics")
@login_required
def analytics_page():
    counts = db.count_sentiments(config.HOTEL_ID)
    trend = db.trend_reviews(config.HOTEL_ID, days=30)
    return render_template("analytics.html", counts=counts, trend=trend)

# API endpoints
@app.post("/api/scrape")
@login_required
def api_scrape():
    # throttle across processes using file timestamp
    now = time.time()
    last = _read_last_ts()
    if now - last < MIN_SCRAPE_INTERVAL:
        return jsonify({"ok": False, "msg": "Terlalu cepat, tunggu beberapa saat"}), 429
    # update timestamp immediately to avoid race
    _write_last_ts(now)
    res = run_scrape_once()
    # if failed, optionally reset timestamp to allow retry sooner
    if not res.get("ok"):
        # small backoff: subtract MIN_SCRAPE_INTERVAL to allow next immediate attempt
        _write_last_ts(last)
    return jsonify(res)

# Scheduler control
@app.post("/api/scheduler/start")
@login_required
def api_sched_start():
    data = request.get_json(force=True)
    minutes = int(data.get("minutes", 15))
    if scheduler.get_job(JOB_ID):
        scheduler.remove_job(JOB_ID)
    scheduler.add_job(scheduled_scrape_job, "interval", minutes=minutes, id=JOB_ID, replace_existing=True)
    return jsonify({"ok": True, "minutes": minutes})

@app.post("/api/scheduler/stop")
@login_required
def api_sched_stop():
    if scheduler.get_job(JOB_ID):
        scheduler.remove_job(JOB_ID)
    return jsonify({"ok": True})

#scheduler status
@app.get("/api/scheduler/status")
@login_required
def api_sched_status():
    job = scheduler.get_job(JOB_ID)
    if job:
        next_run = job.next_run_time
        remaining = None
        if next_run:
            # pastikan semua datetime UTC
            now = datetime.now(timezone.utc)
            next_run = next_run.astimezone(timezone.utc)
            remaining = int((next_run - now).total_seconds())
            if remaining < 0:
                remaining = 0
        return jsonify({
            "ok": True,
            "running": True,
            "interval": job.trigger.interval.total_seconds() // 60,  # menit
            "next_run": next_run.isoformat() if next_run else None,
            "remaining": remaining
        })
    else:
        return jsonify({"ok": True, "running": False})
    
#Halaman subcriber
@app.get("/api/subscribers")
@login_required
def api_get_subs():
    return jsonify(db.get_subscribers())

@app.post("/api/subscribers")
@login_required
def api_add_sub():
    data = request.get_json(force=True)
    chat_id = data.get("chat_id")
    if not chat_id:
        return jsonify({"ok": False, "msg": "chat_id kosong"}), 400
    db.add_subscriber(int(chat_id))
    return jsonify({"ok": True})

@app.route("/api/subscribers/<int:chat_id>", methods=["DELETE"])
@login_required
def api_del_sub(chat_id):
    try:
        db.remove_subscriber(chat_id)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500

@app.get("/api/notifications")
@login_required
def api_get_notifications():
    return jsonify(db.get_notifications(limit=500))

# Analytics APIs
@app.get("/api/analytics/sentiment")
@login_required
def api_analytics_sentiment():
    d = db.count_sentiments(config.HOTEL_ID)
    mapping = [{"label": k, "value": v} for k, v in d.items()]
    return jsonify(mapping)

# Protected trend API analytic
@app.get("/api/analytics/trend")
@login_required
def api_analytics_trend():
    hotel_id = request.args.get("hotel_id", config.HOTEL_ID)
    days = int(request.args.get("days", 30))  # bisa 7 / 30 hari
    rows = db.get_trend_sentiment(hotel_id, days=days)  # ganti ke query baru
    today = date.today()
    lastN = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days-1, -1, -1)]
    data_map = {r["d"].strftime("%Y-%m-%d"): r for r in rows}

    filled = []
    for d in lastN:
        r = data_map.get(d, {"pos": 0, "neg": 0})
        filled.append({
            "date": d,
            "pos": r.get("pos", 0),
            "neg": r.get("neg", 0),
            "total": r.get("pos", 0) + r.get("neg", 0)
        })
    return jsonify(filled)

# api/analytics/keywords
@app.get("/api/analytics/keywords")
def api_keywords():
    lang = request.args.get("lang", "id")  # default: stopwords bahasa Indonesia
    data = db.get_top_keywords(config.HOTEL_ID, limit=10, lang=lang)
    return jsonify({
        "ok": True,
        "positive": [{"word": w, "count": c} for w, c in data["positive"]],
        "negative": [{"word": w, "count": c} for w, c in data["negative"]]
    })

# Analitik Keywords (Word Cloud)
@app.get("/api/analytics/keywords")
@login_required
def api_analytics_keywords():
    """
    Mengambil kata paling sering muncul berdasarkan sentimen
    untuk membentuk word cloud positif dan negatif.
    """
    hotel_id = request.args.get("hotel_id", config.HOTEL_ID)
    data = db.get_top_keywords(hotel_id)

    return jsonify({
        "ok": True,
        "positive": data.get("positive", []),
        "negative": data.get("negative", [])
    })

# Telegram Bot Control from UI
# ROUTES UI
@app.get("/subscribers")
@login_required
def subscribers():
    # nanti ini render subscriber.html yang kamu buat
    return render_template("subscribers.html")

# BOT CONTROL
@app.post("/bot/start")
@login_required
def start_bot():
    global bot_process
    if bot_process is None or not bot_process.is_alive():
        # spawn process, run bot
        bot_process = Process(target=bot_id.run_bot, daemon=True)
        bot_process.start()
        return jsonify({"ok": True, "msg": "Bot started"})
    return jsonify({"ok": False, "msg": "Bot already running"})

@app.post("/bot/stop")
@login_required
def stop_bot():
    global bot_process
    if bot_process and bot_process.is_alive():
        try:
            from pipeline.bot_id import STOP_EVENT
            STOP_EVENT.set()  # beri sinyal ke bot untuk berhenti
            time.sleep(2)     # beri waktu bot menutup loop
        except Exception as e:
            app.logger.warning(f"Gagal kirim stop signal: {e}")

        bot_process.terminate()  # fallback kill jika masih hidup
        bot_process.join(timeout=3)
        if bot_process.is_alive():
            bot_process.kill()
        bot_process = None
        return jsonify({"ok": True, "msg": "Bot stopped"})
    return jsonify({"ok": False, "msg": "Bot not running"})

@app.get("/bot/status")
@login_required
def bot_status():
    global bot_process
    running = bot_process is not None and bot_process.is_alive()
    return jsonify({"running": running})

# Global error handler (API vs Page aware)
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled error: {e}", exc_info=True)
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "msg": "Internal server error"}), 500
    return render_template("error.html", msg=str(e)), 500

# Error.html untuk penanganan kesalahan
@app.errorhandler(404)
def not_found_error(e):
    return render_template("error.html", error_code=404, error_message="Page Not Found"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("error.html", error_code=500, error_message="Internal Server Error"), 500

if __name__ == "__main__":
    # jangan gunakan debug=True jika ingin start multiprocessing di dev
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)