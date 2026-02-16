import os
from dotenv import load_dotenv
load_dotenv()
# App
SECRET_KEY = os.getenv("SECRET_KEY", "12345")
# DATABASE
DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_USER = os.environ.get("DB_USER") or "root"
DB_PASSWORD = os.environ.get("DB_PASSWORD") or ""
DB_NAME = os.environ.get("DB_NAME") or "smart_review"
# Fokus 1 hotel
HOTEL_ID = int(os.getenv("HOTEL_ID", "1"))
HOTEL_NAME = os.getenv("HOTEL_NAME", "Aveta Hotel Malioboro")
# SerpAPI & Google Maps data_id (tempat/hotel)
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "3bea6306886c2e5dea2281bc68bca9cd9908b182974a843f4cf9798fe1d3eb01")
GOOGLE_DATA_ID = os.getenv("GOOGLE_DATA_ID", "0x2e7a59c6e514a5a3:0xbeca960436f8fe88")
# Telegram (hanya dipakai jika kamu ingin broadcast langsung dari UI)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7815909620:AAEZi0vd6oCNAYQeM8VesNFQfj_waYXh68k")
# Rate limit simple untuk tombol Scrape Now
MIN_SCRAPE_INTERVAL_SEC = int(os.getenv("MIN_SCRAPE_INTERVAL_SEC", "30"))
