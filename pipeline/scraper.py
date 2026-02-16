# scraper.py
from serpapi import GoogleSearch
from datetime import datetime, timedelta
import re
from pipeline.mysql_connector import is_new_review, save_hotel_review_raw
import pytz
from deep_translator import GoogleTranslator

# TRANSLASI
translator = GoogleTranslator()
def translate_to_indonesian(text: str) -> str:
    if not text:
        return None
    try:
        return GoogleTranslator(source="auto", target="id").translate(text)
    except Exception as e:
        print("[WARN Translasi gagal]:", e)
        return text
    
# NORMALISASI WAKTU 
WIB = pytz.timezone("Asia/Jakarta")
def parse_review_time(raw_time: str):
    """Konversi waktu review Google Maps ke datetime WIB."""
    if not raw_time:
        return datetime.now(WIB)
    s = raw_time.strip().lower()
    now_wib = datetime.now(WIB)
    # Case: waktu relatif (misal: '12 hours ago', '2 hari lalu')
    rel_match = re.match(r"(\d+|a)\s+(\w+)", s)
    if rel_match:
        value = 1 if rel_match.group(1) == "a" else int(rel_match.group(1))
        unit = rel_match.group(2)
        if "menit" in unit or "minute" in unit:
            dt_wib = now_wib - timedelta(minutes=value)
        elif "jam" in unit or "hour" in unit:
            dt_wib = now_wib - timedelta(hours=value)
        elif "hari" in unit or "day" in unit:
            dt_wib = now_wib - timedelta(days=value)
        elif "minggu" in unit or "week" in unit:
            dt_wib = now_wib - timedelta(weeks=value)
        elif "bulan" in unit or "month" in unit:
            dt_wib = now_wib - timedelta(days=value * 30)
        elif "tahun" in unit or "year" in unit:
            dt_wib = now_wib - timedelta(days=value * 365)
        else:
            dt_wib = now_wib
        print(f"[DEBUG] Waktu relatif ({raw_time}) → WIB: {dt_wib}")
        return dt_wib

    # Case: format tanggal absolut (misal: 'Sep 2, 2025', '20 Agustus 2025')
    try:
        bulan_id = {
            "januari": "January", "februari": "February", "maret": "March",
            "april": "April", "mei": "May", "juni": "June",
            "juli": "July", "agustus": "August", "september": "September",
            "oktober": "October", "november": "November", "desember": "December"
        }
        for indo, eng in bulan_id.items():
            s = s.replace(indo, eng)

        try:
            dt = datetime.strptime(s, "%b %d, %Y")
        except Exception:
            dt = datetime.strptime(s, "%d %B %Y")

        dt_wib = WIB.localize(dt)
        print(f"[DEBUG] Waktu absolut ({raw_time}) → WIB: {dt_wib}")
        return dt_wib
    except Exception:
        pass
    print("[WARN] Gagal parse waktu, fallback ke sekarang WIB.")
    return datetime.now(WIB)

def scrape_latest_review(data_id, serpapi_key):
    params = {
        "engine": "google_maps_reviews",
        "api_key": serpapi_key,
        "data_id": data_id,
        "hl": "id",
        "gl": "id",
        "sort_by": "newestFirst",
        "no_cache": True,
        "limit": 1
    }

    results = GoogleSearch(params).get_dict()
    if "error" in results:
        raise Exception(results["error"])

    reviews = results.get("reviews", [])
    if not reviews:
        return []

    r = reviews[0]
    raw_text = r.get("text") or r.get("snippet") or r.get("content")
    text = raw_text.strip() if raw_text else None
    translated_text = translate_to_indonesian(text) if text else None

    return [{
        "text": translated_text,
        "raw_text": raw_text,
        "time": r.get("timestamp") or r.get("date") or r.get("time_ago"),
        "rating": r.get("rating", 0),
        "user": (
            r["user"]["name"] if isinstance(r.get("user"), dict) and "name" in r["user"]
            else str(r.get("user", "Unknown"))
        )
    }]


if __name__ == "__main__":
    serpapi_key = "3bea6306886c2e5dea2281bc68bca9cd9908b182974a843f4cf9798fe1d3eb01"  # ganti dengan API key SerpAPI
    data_id = "0x2e7a59c6e514a5a3:0xbeca960436f8fe88"

    try:
        reviews = scrape_latest_review(data_id, serpapi_key)
        if not reviews:
            print("Tidak ada review ditemukan.")
        else:
            latest = reviews[0]
            parsed_time = parse_review_time(latest.get("time"))

            if is_new_review(latest["text"]):
                # Simpan waktu dalam WIB langsung (bukan UTC)
                review_id = save_hotel_review_raw(
                    hotel_id=1,
                    review_text=latest["text"],
                    review_date=parsed_time,
                    rating=latest["rating"],
                    user_name=latest["user"]
                )                            
                waktu_wib = parsed_time.strftime("%d/%m/%Y %H:%M:%S")
                print(f"🆕 Review baru disimpan (id={review_id})")
                print(f"🕒 Waktu review (WIB): {waktu_wib}")
                print(f"🧑 User: {latest['user']}")
                print(f"⭐ Rating: {latest['rating']}")
                print(f"💬 Review: {latest['text']}")
            else:
                print("Review sudah ada di DB, skip.")
    except Exception as e:
        print("[ERROR Scraper]:", e)
