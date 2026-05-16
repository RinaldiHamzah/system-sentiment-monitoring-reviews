# Hotel Review Sentiment Monitoring

Hotel Review Sentiment Monitoring adalah aplikasi web untuk membantu pemilik atau pengelola hotel memahami kualitas layanan berdasarkan ulasan pelanggan. Sistem ini menggabungkan scraping review Google Maps, klasifikasi sentimen berbasis machine learning, dashboard analitik, scheduler otomatis, panel admin, dan notifikasi Telegram dalam satu alur kerja yang terintegrasi.

Project ini dikembangkan sebagai tugas akhir dengan fokus pada studi kasus monitoring reputasi hotel. Arsitektur sistem dirancang dengan aturan **1 user = 1 hotel**, sehingga setiap akun dapat mengelola data hotel, ulasan, analitik, dan notifikasi secara terpisah.

## Highlight

- **Monitoring ulasan hotel berbasis data**: review dikumpulkan, disimpan, dianalisis, dan divisualisasikan melalui dashboard.
- **Analisis sentimen otomatis**: sistem melakukan klasifikasi sentimen menggunakan model Naive Bayes dan SVM.
- **Scraping Google Maps**: pengambilan data review dilakukan berdasarkan `place_id` melalui SerpAPI.
- **Dashboard analitik**: tersedia ringkasan rating, tren review, distribusi sentimen, dan keyword penting.
- **Notifikasi Telegram**: sistem dapat mengirim broadcast untuk informasi atau pembaruan tertentu.
- **Scheduler scraping**: proses pengambilan review dapat dijalankan otomatis per hotel.
- **Panel admin**: admin dapat memantau dan mengelola data utama sistem.
- **Ekspor data**: review dapat diekspor ke format CSV atau Excel untuk kebutuhan laporan.

## Fitur Utama

### Untuk User Hotel

- Registrasi akun sekaligus registrasi data hotel.
- Login, logout, dan reset password.
- Mengelola data hotel yang terhubung dengan akun.
- Menjalankan scraping review Google Maps.
- Melihat daftar review dan hasil prediksi sentimen.
- Memantau statistik review melalui dashboard.
- Mengelola subscriber Telegram.
- Mengekspor data review.

### Untuk Admin

- Monitoring data user dan hotel.
- Melihat data review lintas hotel.
- Mengelola data utama sistem.
- Memantau aktivitas scraping, notifikasi, dan integrasi sistem.

### Machine Learning

- Preprocessing data review.
- Ekstraksi fitur menggunakan TF-IDF.
- Prediksi sentimen menggunakan Naive Bayes dan SVM.
- Penyimpanan model menggunakan `joblib` dalam format `.pkl`.

## Teknologi

| Area | Teknologi |
| --- | --- |
| Backend | Flask |
| Database | MySQL / MariaDB |
| Scheduler | APScheduler |
| Machine Learning | scikit-learn, joblib |
| Frontend | HTML, CSS, JavaScript, Jinja Templates |
| Scraping | SerpAPI Google Maps Reviews |
| Notifikasi | Telegram Bot API |

## Arsitektur Singkat

```text
APP TA/
|- app.py                 # Route halaman, API, scheduler, dan kontrol bot
|- config.py              # Konfigurasi berbasis environment variable
|- schema.sql             # Struktur database utama
|- requirements.txt       # Daftar dependency Python
|- pipeline/              # Modul scraping, prediksi, koneksi DB, dan utilitas
|- templates/             # Template halaman HTML
|- static/                # Asset CSS, JavaScript, dan gambar
|- model_ml/              # Model machine learning untuk inference
|- analisis/              # Notebook dan artefak analisis eksperimen
```

Alur utama sistem:

1. User mendaftarkan akun dan data hotel.
2. Sistem mengambil review Google Maps berdasarkan `place_id`.
3. Review disimpan ke database.
4. Model machine learning melakukan prediksi sentimen.
5. Dashboard menampilkan ringkasan rating, sentimen, tren, dan keyword.
6. Scheduler dan Telegram membantu proses monitoring berjalan lebih otomatis.

## Prasyarat

Pastikan environment berikut sudah tersedia:

- Python 3.10 atau lebih baru.
- MySQL atau MariaDB.
- Git untuk clone dan kolaborasi.
- Akun SerpAPI untuk fitur scraping.
- Bot Telegram jika ingin mengaktifkan fitur notifikasi.

## Instalasi

Clone repository:

```bash
git clone https://github.com/RinaldiHamzah/system-sentiment-monitoring-reviews.git
cd system-sentiment-monitoring-reviews
```

Buat virtual environment:

```bash
python -m venv env
```

Aktifkan virtual environment:

```bash
# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

## Konfigurasi Environment

Buat file `.env` di root project. Gunakan `.env.example` sebagai referensi.

```env
SECRET_KEY=replace-with-strong-random-secret
APP_HOST=0.0.0.0
APP_PORT=5000

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=monitoring_review

SERPAPI_KEY=your_serpapi_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

MIN_SCRAPE_INTERVAL_SEC=30
DATA_DIR=.
```

Catatan keamanan:

- Jangan commit file `.env`.
- Simpan API key dan token hanya di environment lokal.
- `SERPAPI_KEY` wajib untuk fitur scraping.
- `TELEGRAM_BOT_TOKEN` bersifat opsional jika fitur bot tidak digunakan.

## Setup Database

Buat database:

```sql
CREATE DATABASE IF NOT EXISTS monitoring_review
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Import skema database:

```bash
mysql -u root -p monitoring_review < schema.sql
```

Jika menggunakan MariaDB/MySQL shell:

```sql
USE monitoring_review;
SOURCE schema.sql;
```

## Menjalankan Aplikasi

Jalankan aplikasi Flask:

```bash
python app.py
```

Akses aplikasi melalui browser:

- Login: `http://127.0.0.1:5000/login`
- Register: `http://127.0.0.1:5000/register`
- Dashboard: `http://127.0.0.1:5000/dashboard`

## Endpoint Utama

### Halaman

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/login` | Halaman login |
| GET | `/register` | Halaman registrasi user dan hotel |
| GET | `/dashboard` | Dashboard user hotel |
| GET | `/reviews` | Daftar review |
| GET | `/analytics` | Analitik sentimen dan rating |
| GET | `/subscribers` | Manajemen subscriber Telegram |
| GET | `/notifications` | Log notifikasi |
| GET | `/admin/dashboard` | Dashboard admin |
| GET | `/admin/data` | Manajemen data admin |

### API

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| GET | `/api/reviews` | Mengambil data review |
| GET | `/api/notifications` | Mengambil data notifikasi |
| POST | `/api/scrape` | Menjalankan scraping review |
| POST | `/api/scheduler/start` | Menyalakan scheduler |
| POST | `/api/scheduler/stop` | Mematikan scheduler |
| GET | `/api/scheduler/status` | Melihat status scheduler |
| GET | `/api/subscribers` | Mengambil subscriber Telegram |
| POST | `/api/subscribers` | Menambah subscriber Telegram |
| DELETE | `/api/subscribers/<chat_id>` | Menghapus subscriber Telegram |
| GET | `/api/analytics/sentiment` | Data analitik sentimen |
| GET | `/api/analytics/rating` | Data analitik rating |
| GET | `/api/analytics/trend` | Data tren review |
| GET | `/api/analytics/keywords` | Data keyword review |

### Bot Control

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| POST | `/bot/start` | Menyalakan bot Telegram |
| POST | `/bot/stop` | Mematikan bot Telegram |
| GET | `/bot/status` | Melihat status bot Telegram |

## Demo Aplikasi

Demo aplikasi menampilkan alur sistem mulai dari input dan pengambilan ulasan, pemrosesan TF-IDF, klasifikasi sentimen menggunakan Naive Bayes dan SVM, hingga visualisasi hasil pada dashboard analitik.

[Tonton demo aplikasi](https://drive.google.com/file/d/1oA91pVq13Lb6Kn3RAzjQRKhDnKx1sC0d/view?usp=sharing)

## Troubleshooting

### `mysql` tidak dikenali di PowerShell

Gunakan path penuh ke binary MySQL. Contoh untuk XAMPP:

```powershell
& "C:\xampp\mysql\bin\mysql.exe" -u root -p
```

### Model machine learning tidak ditemukan

Pastikan file model tersedia di direktori yang digunakan aplikasi:

- `naive_bayes_model.pkl`
- `SVM_model.pkl`
- `vectorizer.pkl`

### Scraping tidak berjalan

Periksa beberapa hal berikut:

- `SERPAPI_KEY` sudah diisi di file `.env`.
- Koneksi internet aktif.
- `place_id` hotel valid.
- Response endpoint `/api/scrape` tidak mengembalikan error.

### Bot Telegram gagal start

Periksa beberapa hal berikut:

- `TELEGRAM_BOT_TOKEN` sudah benar.
- Bot tidak sedang berjalan di proses lain.
- Aplikasi sudah direstart setelah token diperbarui.

## Kontribusi

Kontribusi sangat terbuka untuk pengembangan project ini. Beberapa area yang bisa dikembangkan:

- Peningkatan kualitas model sentimen.
- Penambahan visualisasi analitik.
- Optimasi pipeline scraping dan scheduler.
- Perbaikan UI/UX dashboard.
- Penambahan test otomatis.
- Dokumentasi deployment.
- Integrasi sumber review lain selain Google Maps.

Alur kontribusi yang disarankan:

1. Fork repository ini.
2. Buat branch fitur atau perbaikan.
3. Lakukan perubahan secara terarah.
4. Pastikan aplikasi tetap dapat dijalankan.
5. Buat pull request dengan deskripsi yang jelas.

## Lisensi

Project ini dikembangkan untuk kebutuhan akademik dan pembelajaran. Jika ingin menggunakan atau mengembangkan ulang project ini, harap cantumkan kredit yang sesuai kepada pembuat repository.
