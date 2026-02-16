# pipeline.py
import json
from pipeline.model_predict import ModelPredict
from pipeline.scraper import scrape_latest_review
from pipeline.notif_telegram import send_telegram_to_user
from pipeline.scraper import scrape_latest_review, parse_review_time as normalize_review_time
from pipeline.mysql_connector import (
    save_hotel_review,
    save_sentiment_review,
    log_notification,
    get_connection,
    get_trend_sentiment
)

# Helper Functions
def is_new_review(review_text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM hotel_reviews WHERE review_text = %s", (review_text,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count == 0

def get_subscribed_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM telegram_users WHERE subscribed=TRUE")
    chat_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return chat_ids

def normalize_sentiment(label, rating=None):
    if label is None:
        label = ""
    t = str(label).strip().lower()
    pos_tokens = ("positive", "positif")
    neg_tokens = ("negative", "negatif")

    if any(t.startswith(x) for x in pos_tokens):
        return "Positive"
    if any(t.startswith(x) for x in neg_tokens):
        return "Negative"
    if rating is not None:
        return "Positive" if rating >= 4 else "Negative"
    return "Positive"

# Pipeline 
def run_pipeline():
    serpapi_key = "3bea6306886c2e5dea2281bc68bca9cd9908b182974a843f4cf9798fe1d3eb01"
    data_id = "0x2e7a59c6e514a5a3:0xbeca960436f8fe88"

    try:
        reviews = scrape_latest_review(data_id, serpapi_key)
        if not reviews:
            print("[INFO] Tidak ada review terbaru.")
            return
        
        latest_review = reviews[0]
        review_text = latest_review.get("text", "")
        rating = latest_review.get("rating", None)
        user = latest_review.get("user", "Anonim")

        # Cek duplikat
        if not is_new_review(review_text):
            print("Review sudah ada di DB, skip pipeline.")
            return

        # Prediksi Sentimen
        model = ModelPredict()
        if review_text and review_text.strip():
            sentiment_nb = normalize_sentiment(model.predict_nb(review_text), rating)
            sentiment_svm = normalize_sentiment(model.predict_svm(review_text), rating)
        else:
            if rating and rating <= 3:
                sentiment_nb = sentiment_svm = "Negative"
            else:
                sentiment_nb = sentiment_svm = "Positive"
            review_text = f"(Tidak ada teks, hanya rating ⭐ {rating})"
        
        # Simpan ke DB
        parsed_time = normalize_review_time(latest_review.get("time")) # Normalisasi waktu
        review_id = save_hotel_review(
            hotel_id=1,
            user_name=user,
            review_text=review_text,
            rating=rating,
             review_date=parsed_time,
            source="Google Maps"
        )
        save_sentiment_review(review_id, sentiment_nb, sentiment_svm)

        # Kirim notifikasi ke tiap user
        chat_ids = get_subscribed_users()
        for chat_id in chat_ids:
            send_telegram_to_user(
                chat_id=chat_id,
                review_text=review_text,
                sentiment_nb=sentiment_nb,
                sentiment_svm=sentiment_svm,
                rating=rating,
                user=user
            )
            log_notification(review_id, chat_id, status="sent")

        # Simpan ke JSON cache
        latest_review["sentiment_nb"] = sentiment_nb
        latest_review["sentiment_svm"] = sentiment_svm
        with open("latest_review.json", "w", encoding="utf-8") as f:
            json.dump(latest_review, f, ensure_ascii=False, indent=2)

        print("Pipeline sukses")
        print("   - Naive Bayes:", sentiment_nb)
        print("   - SVM:", sentiment_svm)
        print("   - Stored review_id:", review_id)

    except Exception as e:
        print("[ERROR Pipeline]:", e)
        for chat_id in get_subscribed_users():
            send_telegram_to_user(
                chat_id=chat_id,
                review_text="Terjadi kesalahan dalam pipeline.",
                sentiment_nb="Error",
                sentiment_svm="Error",
                rating=None,
                user="System"
            )
            log_notification(None, chat_id, status="error")

if __name__ == "__main__":
    run_pipeline()
