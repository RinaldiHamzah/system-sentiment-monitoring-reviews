import os
from dotenv import load_dotenv
load_dotenv()
# App
SECRET_KEY = os.getenv("SECRET_KEY", "xxxxxxxxxxx") #password app
# DATABASE
DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_USER = os.environ.get("DB_USER") or "root"
DB_PASSWORD = os.environ.get("DB_PASSWORD") or ""
DB_NAME = os.environ.get("DB_NAME") or "smart_review"
# Fokus 1 hotel
HOTEL_ID = int(os.getenv("HOTEL_ID", "1"))
HOTEL_NAME = os.getenv("HOTEL_NAME", "Aveta Hotel Malioboro")
# SerpAPI & Google Maps data_id (tempat/hotel)
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") # ganti dengan SerpAPI 
GOOGLE_DATA_ID = os.getenv("GOOGLE_DATA_ID", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") # id lokasi
# Telegram (hanya dipakai jika kamu ingin broadcast langsung dari UI)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") # daftar di Bot Father Telegram
# Rate limit simple untuk tombol Scrape Now
MIN_SCRAPE_INTERVAL_SEC = int(os.getenv("MIN_SCRAPE_INTERVAL_SEC", "30"))
