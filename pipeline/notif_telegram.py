# notif_telegram.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import threading
import mysql.connector

BOT_TOKEN = "7815909620:AAEZi0vd6oCNAYQeM8VesNFQfj_waYXh68k"

# Koneksi Database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="",        
        database="smart_review"
    )

# START Command → Simpan chat_id ke DB
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"[INFO] User Chat_id: {chat_id}")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO telegram_users (chat_id, subscribed) VALUES (%s, TRUE) "
            "ON DUPLICATE KEY UPDATE subscribed=TRUE",
            (chat_id,)
        )
        conn.commit()
        await update.message.reply_text(
            "Hello 🤖 Kamu sudah terdaftar untuk menerima notifikasi review terbaru!"
        )
    except Exception as e:
        print("[ERROR] DB:", e)
    finally:
        cursor.close()
        conn.close()

#Kirim pesan mentah ke satu user
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"[ERROR] gagal kirim ke {chat_id}: {response.text}")
        else:
            print(f"[OK] pesan terkirim ke {chat_id}")
    except Exception as e:
        print(f"[ERROR] Exception kirim ke {chat_id}: {e}")

# Kirim notifikasi ke satu user (pakai waktu Google Maps)
def send_telegram_to_user(chat_id, review_id, review_text, sentiment_nb, sentiment_svm, rating=None, user='System'):
    # Ambil waktu asli review dari DB
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT review_date FROM hotel_reviews WHERE review_id=%s", (review_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row and row["review_date"]:
        review_time = row["review_date"].strftime('%d/%m/%Y %H:%M:%S')
    else:
        review_time = "-"  # fallback jika kosong

    message = f"""
📢 <b>Review Baru</b>
👤 <b>User:</b> {user}
⭐ <b>Rating:</b> {rating}
📝 <b>Review:</b> {review_text[:400]}
🤖 <b>Naive Bayes:</b> {sentiment_nb}
⚡ <b>Support Vector Machine:</b> {sentiment_svm}
🕒 <b>Waktu:</b> {review_time}
"""
    send_message(chat_id, message)

# Broadcast ke semua user
def broadcast_telegram(review_id, review_text, sentiment_nb, sentiment_svm, rating=None, user='System'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM telegram_users WHERE subscribed=TRUE")
    chat_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    threads = []
    for chat_id in chat_ids:
        t = threading.Thread(
            target=send_telegram_to_user,
            args=(chat_id, review_id, review_text, sentiment_nb, sentiment_svm, rating, user)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

# Jalankan Bot 
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("[INFO] Bot Telegram berjalan...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()

