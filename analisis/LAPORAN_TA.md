# LAPORAN TUGAS AKHIR

## Rancang Bangun Sistem Monitoring Ulasan Hotel dan Analisis Sentimen Berbasis Machine Learning

### Identitas Mahasiswa
- Nama: [Isi Nama Anda]
- NIM: [Isi NIM]
- Program Studi: [Isi Prodi]
- Fakultas: [Isi Fakultas]
- Perguruan Tinggi: [Isi Kampus]
- Tahun: 2026

## Abstrak
Ulasan pelanggan pada Google Maps memiliki peran penting dalam membentuk reputasi hotel. Ulasan dengan sentimen negatif yang tidak ditangani secara cepat dapat menurunkan citra layanan. Penelitian ini bertujuan merancang dan mengimplementasikan sistem monitoring sentimen ulasan pelanggan berbasis web pada Aveta Hotel Malioboro. Sistem dikembangkan menggunakan Flask, basis data MySQL/MariaDB, serta notifikasi Telegram untuk distribusi informasi otomatis. Data historis penelitian diperoleh melalui proses scraping ulasan dengan total 2.449 ulasan, sedangkan monitoring operasional menggunakan integrasi SerpAPI. Proses analisis sentimen menggunakan pembobotan TF-IDF dengan dua algoritma klasifikasi, yaitu Complement Naive Bayes dan Support Vector Machine (Linear SVM), pada dua skenario eksperimen: tidak balance dan balance (resample) pada data latih. Hasil evaluasi terbaru menunjukkan model SVM pada skenario balance memberikan akurasi tertinggi (0.9540), sedangkan SVM pada skenario tidak balance memberikan balanced accuracy tertinggi (0.8950). Sistem yang dikembangkan juga menyediakan autentikasi pengguna, dashboard monitoring, analitik tren, dan scheduler scraping periodik per hotel, sehingga membantu pengelola merespons ulasan pelanggan secara lebih cepat, terstruktur, dan berbasis data.

Kata kunci: monitoring ulasan, analisis sentimen, Flask, SVM, Naive Bayes, TF-IDF.

## BAB I Pendahuluan

### 1.1 Latar Belakang
Platform ulasan daring menghasilkan data opini pelanggan dalam jumlah besar. Pada konteks perhotelan, ulasan tersebut berisi informasi penting tentang kualitas layanan, fasilitas, kebersihan, dan pengalaman tamu. Pengolahan manual terhadap data ulasan tidak efisien dan berisiko menimbulkan keterlambatan pengambilan keputusan. Oleh karena itu, dibutuhkan sistem yang mampu mengotomasi pengambilan ulasan, klasifikasi sentimen, serta penyajian analitik secara near real-time.

### 1.2 Rumusan Masalah
- Bagaimana membangun sistem monitoring ulasan hotel berbasis web yang terintegrasi dengan analisis sentimen?
- Bagaimana performa model Naive Bayes dan SVM pada klasifikasi sentimen ulasan hotel?
- Bagaimana sistem menyajikan informasi analitik agar mendukung keputusan pengguna hotel?

### 1.3 Batasan Masalah
- Data ulasan diambil dari Google Maps.
- Klasifikasi sentimen bersifat biner: POSITIF dan NEGATIF.
- Algoritma klasifikasi: Multinomial Naive Bayes dan Linear SVM.
- Arsitektur aplikasi menerapkan aturan 1 user = 1 hotel.

### 1.4 Tujuan Penelitian
- Mengembangkan aplikasi monitoring ulasan hotel berbasis web.
- Menerapkan pipeline klasifikasi sentimen berbasis TF-IDF + machine learning.
- Membandingkan performa model pada skenario tidak balance dan balance (resample).
- Mengintegrasikan model terbaik ke sistem produksi aplikasi.

### 1.5 Manfaat Penelitian
- Mempermudah monitoring sentimen pelanggan bagi pengelola hotel.
- Memberikan insight cepat terhadap kualitas layanan.
- Menjadi referensi implementasi sistem analitik ulasan pada domain serupa.

## BAB II Tinjauan Pustaka

### 2.1 Monitoring Ulasan Pelanggan
Monitoring ulasan pelanggan adalah proses pengumpulan, penyimpanan, dan analisis opini pengguna dari platform digital untuk mendukung evaluasi layanan.

### 2.2 Analisis Sentimen
Analisis sentimen mengelompokkan opini teks ke dalam polaritas sentimen. Pada penelitian ini digunakan dua label: POSITIF dan NEGATIF.

### 2.3 Text Preprocessing
Tahapan preprocessing meliputi normalisasi, stopword filtering, dan stemming untuk mengurangi noise pada teks ulasan.

### 2.4 TF-IDF
TF-IDF merepresentasikan dokumen teks sebagai fitur numerik berdasarkan frekuensi istilah terhadap koleksi dokumen.

### 2.5 Multinomial Naive Bayes
Algoritma probabilistik untuk klasifikasi teks dengan komputasi ringan dan baseline yang baik.

### 2.6 Support Vector Machine (Linear SVM)
Algoritma klasifikasi yang efektif untuk data berdimensi tinggi seperti representasi teks TF-IDF.

### 2.7 Balancing Data
Balancing data digunakan untuk menyeimbangkan distribusi kelas pada data latih. Pada penelitian ini, balancing dilakukan dengan metode random upsampling kelas minoritas menggunakan `resample` sehingga jumlah data kelas minoritas disetarakan dengan kelas mayoritas.

## BAB III Metodologi Penelitian

### 3.1 Metode Penelitian
Metode yang digunakan adalah rancang bangun sistem (design and implementation) dengan tahapan: analisis kebutuhan, perancangan arsitektur, implementasi aplikasi, eksperimen model sentimen, integrasi model, dan pengujian sistem.

### 3.2 Sumber Data
- Ulasan hotel dari Google Maps (scraping melalui SerpAPI).
- Data operasional aplikasi disimpan pada MySQL/MariaDB.

### 3.3 Alur Umum Sistem
1. User mendaftarkan akun beserta data hotel (termasuk place_id/link Google Maps).
2. Sistem melakukan scraping ulasan terbaru sesuai hotel aktif.
3. Teks ulasan diprediksi oleh model Naive Bayes dan SVM.
4. Hasil disimpan ke tabel review dan sentiment.
5. Dashboard menampilkan statistik, tren, rating, dan keyword.
6. Jika ada subscriber, sistem mengirim notifikasi Telegram.
7. Scheduler menjalankan scraping otomatis berkala per hotel.

### 3.4 Teknologi yang Digunakan
- Backend: Flask
- Database: MySQL/MariaDB
- Scheduler: APScheduler
- ML Inference: scikit-learn, joblib
- Frontend: HTML, CSS, JavaScript (Jinja2)
- Integrasi eksternal: SerpAPI dan Telegram Bot API

### 3.5 Struktur Proyek
- `app.py`: route halaman, API, autentikasi, scheduler, dan bot control.
- `pipeline/`: modul scraping, prediksi model, koneksi DB, pipeline orchestration, notifikasi.
- `schema.sql`: skema basis data utama.
- `templates/` dan `static/`: antarmuka dashboard dan visualisasi.
- `analisis/`: eksperimen preprocessing, pelabelan, training, evaluasi model.

## BAB IV ANALISIS DAN PERANCANGAN SISTEM

### 4.1 Analisis Sistem

#### 4.1.1 Analisis Sistem yang Berjalan
Sistem pemantauan ulasan pada hotel saat ini masih mengandalkan platform Google Maps secara langsung. Kondisi tersebut menimbulkan beberapa keterbatasan, yaitu: (1) tidak tersedia mekanisme pengambilan data ulasan secara terstruktur, (2) tidak ada klasifikasi sentimen otomatis, (3) pemantauan ulasan dilakukan manual, dan (4) tidak tersedia notifikasi terintegrasi untuk mempercepat respons manajemen terhadap ulasan baru.

#### 4.1.2 Analisis Sistem yang Diusulkan
Berdasarkan permasalahan tersebut, diusulkan sistem monitoring ulasan hotel berbasis web yang terintegrasi dengan analisis sentimen. Sistem ini memanfaatkan scraping ulasan Google Maps melalui SerpAPI, klasifikasi sentimen menggunakan model Naive Bayes dan Support Vector Machine (SVM), penyimpanan hasil ke basis data MySQL/MariaDB, serta notifikasi Telegram untuk distribusi informasi otomatis.

Sistem yang diusulkan menerapkan prinsip 1 user terhubung ke 1 hotel. Setiap data operasional diisolasi berdasarkan `hotel_id` agar pengguna hanya mengakses data hotel miliknya.

### 4.2 Analisis Kebutuhan Sistem

#### 4.2.1 Kebutuhan Fungsional
Kebutuhan fungsional sistem meliputi:
1. Pengelolaan autentikasi pengguna: register, login, logout, dan reset password.
2. Pengelolaan data hotel saat registrasi pengguna.
3. Pengambilan ulasan terbaru dari Google Maps berdasarkan `place_id`.
4. Klasifikasi sentimen ulasan ke label POSITIF/NEGATIF menggunakan model NB dan SVM.
5. Penyimpanan data ulasan dan hasil sentimen ke basis data.
6. Penyajian dashboard monitoring (ringkasan review, sentimen, rating, tren, keyword).
7. Pengelolaan subscriber Telegram per hotel.
8. Pengiriman notifikasi otomatis saat review baru terdeteksi.
9. Penjadwalan scraping berkala per hotel (start/stop/status).

#### 4.2.2 Kebutuhan Nonfungsional
Kebutuhan nonfungsional sistem meliputi:
1. Kinerja: proses scraping dan prediksi harus berjalan stabil untuk pemantauan berkala.
2. Keandalan: sistem mampu menangani kegagalan API eksternal (SerpAPI/Telegram) tanpa menghentikan layanan utama.
3. Keamanan: token dan secret disimpan pada `.env`; akses endpoint dibatasi middleware role.
4. Skalabilitas: struktur data dan job scheduler mendukung penambahan hotel.
5. Usability: antarmuka dashboard mudah dipahami oleh pengguna non-teknis.

### 4.3 Perancangan Arsitektur Sistem
Sistem dirancang dengan pendekatan web application berbasis Flask (server-side rendering Jinja). Komponen utama sistem adalah:
1. Lapisan presentasi: `templates/` dan `static/`.
2. Lapisan aplikasi: `app.py` (route halaman, API, autentikasi, scheduler, kontrol bot).
3. Lapisan pipeline: `pipeline/` (scraper, model inferensi, konektor database, notifikasi).
4. Lapisan data: MySQL/MariaDB (`schema.sql`).

Alur utama sistem:
1. User login ke akun yang terhubung dengan hotel miliknya.
2. Sistem memicu scraping manual/otomatis.
3. Ulasan baru diproses (normalisasi waktu, deduplikasi, klasifikasi sentimen).
4. Hasil disimpan ke database dan ditampilkan di dashboard.
5. Notifikasi dikirim ke subscriber Telegram sesuai hotel terkait.

### 4.4 Perancangan Basis Data
Basis data terdiri dari enam tabel utama:
1. `hotels`: menyimpan profil hotel, `place_id`, interval scraping, dan status aktif.
2. `users`: menyimpan akun dan relasi ke hotel.
3. `hotel_reviews`: menyimpan ulasan mentah hasil scraping.
4. `sentiment_reviews`: menyimpan hasil klasifikasi sentimen.
5. `telegram_users`: menyimpan subscriber Telegram per hotel.
6. `notifications`: menyimpan log pengiriman notifikasi.

Relasi utama:
1. `hotels` berelasi 1:N terhadap `users`, `hotel_reviews`, `sentiment_reviews`, `telegram_users`, `notifications`.
2. `hotel_reviews` berelasi ke `sentiment_reviews` dan `notifications`.
3. `notifications` berelasi komposit ke `telegram_users` (`chat_id`, `hotel_id`).

### 4.5 Perancangan Modul Sistem
Modul sistem yang dirancang mencakup:
1. Modul autentikasi dan manajemen user.
2. Modul scraping ulasan Google Maps.
3. Modul klasifikasi sentimen berbasis model machine learning.
4. Modul dashboard dan analitik.
5. Modul scheduler scraping berkala.
6. Modul notifikasi Telegram.

### 4.6 Ringkasan Perancangan
Perancangan sistem menghasilkan rancangan yang terintegrasi antara pengambilan data ulasan, analisis sentimen, penyimpanan data, visualisasi analitik, dan notifikasi otomatis. Rancangan ini menjadi dasar implementasi pada Bab V.

## BAB V IMPLEMENTASI, HASIL, DAN PEMBAHASAN

### 5.1 Implementasi Sistem

#### 5.1.1 Implementasi Backend
Implementasi backend dilakukan pada `app.py` menggunakan Flask. Sistem mengelola route halaman dan API, middleware otorisasi pengguna, integrasi database, kontrol scheduler, serta kontrol Telegram bot.

#### 5.1.2 Implementasi Pipeline Monitoring Sentimen
Pipeline utama berjalan pada `pipeline/pipeline.py` dengan tahapan:
1. Ambil konfigurasi hotel dan `place_id`.
2. Scrape review terbaru dari Google Maps menggunakan SerpAPI.
3. Parsing waktu ulasan ke zona waktu WIB.
4. Cek duplikasi data review.
5. Prediksi sentimen menggunakan NB dan SVM.
6. Simpan hasil ke tabel review dan sentimen.
7. Kirim notifikasi Telegram ke subscriber terkait.
8. Simpan log notifikasi.

#### 5.1.3 Implementasi Model Analisis Sentimen
Model inferensi berada pada `pipeline/model_predict.py` dan memuat tiga artefak: `naive_bayes_model.pkl`, `SVM_model.pkl`, dan `vectorizer.pkl`. Representasi teks menggunakan TF-IDF dan output dinormalisasi ke label POSITIF/NEGATIF.

Catatan metodologis: pelabelan dataset pelatihan menggunakan model transformer pra-latih (weak supervision), sehingga label referensi bukan anotasi manual penuh.

#### 5.1.4 Implementasi Scheduler
Scheduler menggunakan APScheduler (`BackgroundScheduler`) dengan job per `hotel_id`. Pendekatan ini memungkinkan scraping periodik dengan interval yang dapat dikontrol.

Karakter layanan sistem adalah near real-time karena pembaruan data berbasis interval scheduler, bukan streaming kontinu.

#### 5.1.5 Implementasi Antarmuka
Antarmuka dikembangkan menggunakan Jinja template dan Bootstrap. Halaman utama yang diimplementasikan mencakup login/register, dashboard, analytics, reviews, subscribers, dan notifications.

#### 5.1.6 Implementasi Keamanan Dasar
1. Secret key dan token API disimpan pada file `.env`.
2. Akses endpoint dibatasi berdasarkan role pengguna.
3. Isolasi data diterapkan berdasarkan `hotel_id`.

### 5.2 Hasil
Hasil implementasi menunjukkan bahwa:
1. Sistem berhasil melakukan scraping ulasan terbaru per hotel.
2. Sistem berhasil mengklasifikasi sentimen ulasan menggunakan dua model (NB dan SVM).
3. Hasil klasifikasi tersimpan dan ditampilkan pada dashboard serta halaman histories.
4. Scheduler start/stop/status berjalan sesuai interval yang ditentukan.
5. Notifikasi Telegram berhasil dikirim dan dicatat pada log notifikasi.

Hasil evaluasi model pada eksperimen:
1. Skenario tidak balance (baseline):
   - Naive Bayes: Accuracy 0.9494; F1 Macro 0.8090; Balanced Accuracy 0.7640.
   - SVM: Accuracy 0.9425; F1 Macro 0.8404; Balanced Accuracy 0.8950.
2. Skenario balance (resample):
   - Naive Bayes: Accuracy 0.9402; F1 Macro 0.8210; Balanced Accuracy 0.8448.
   - SVM: Accuracy 0.9540; F1 Macro 0.8405; Balanced Accuracy 0.8155.

### 5.3 Pembahasan
Berdasarkan implementasi dan hasil pengujian, sistem yang dibangun telah memenuhi tujuan penelitian, yaitu menyediakan solusi monitoring ulasan hotel yang terintegrasi dengan analisis sentimen dan notifikasi otomatis. Sistem tidak hanya mampu mengambil data ulasan terbaru, tetapi juga dapat mengolah, mengklasifikasikan, menyimpan, dan menyajikan hasil analisis secara terstruktur melalui dashboard dan notifikasi Telegram.

Dari sisi model, hasil eksperimen menunjukkan bahwa tidak ada satu skenario yang unggul mutlak pada seluruh metrik evaluasi. Model SVM pada skenario balance menghasilkan akurasi tertinggi sebesar 0.9540, yang menunjukkan performa klasifikasi keseluruhan paling baik pada data uji. Akan tetapi, model SVM pada skenario tidak balance justru menghasilkan balanced accuracy tertinggi sebesar 0.8950, yang menunjukkan kemampuan yang lebih baik dalam menjaga keseimbangan performa antar kelas pada kondisi distribusi data asli.

Pada model Naive Bayes, penerapan balancing memberikan pengaruh yang cukup jelas. Akurasi Naive Bayes menurun dari 0.9494 menjadi 0.9402, tetapi nilai F1 Macro meningkat dari 0.8090 menjadi 0.8210 dan balanced accuracy meningkat dari 0.7640 menjadi 0.8448. Hal ini menunjukkan bahwa balancing membantu Naive Bayes dalam mengenali kelas minoritas dengan lebih baik, meskipun ketepatan prediksi keseluruhan sedikit menurun. Dengan demikian, hasil penelitian ini menegaskan bahwa evaluasi model klasifikasi pada data tidak seimbang tidak cukup hanya didasarkan pada akurasi, tetapi juga perlu mempertimbangkan metrik lain seperti F1 Macro dan balanced accuracy.

Jika ditinjau dari sisi implementasi sistem, integrasi antar modul utama, yaitu scraping, inferensi model, penyimpanan basis data, dashboard analitik, scheduler, dan notifikasi Telegram, telah berjalan secara konsisten. Hal ini menunjukkan bahwa model hasil eksperimen tidak hanya berhenti pada tahap evaluasi akademik, tetapi juga berhasil diimplementasikan dalam konteks aplikasi operasional yang dapat digunakan sebagai alat bantu monitoring ulasan hotel.

Namun, terdapat beberapa batasan:
1. Cakupan data masih terbatas pada domain hotel tertentu.
2. Label pelatihan berbasis weak supervision berpotensi membawa bias model pelabel.
3. Keandalan sistem dipengaruhi oleh layanan eksternal (SerpAPI dan Telegram).
4. Pendekatan near real-time bergantung pada konfigurasi interval scheduler.

Dengan demikian, pengembangan lanjutan dapat diarahkan pada perluasan dataset, validasi manual sebagian data, evaluasi model pada domain yang lebih beragam, serta peningkatan observability dan ketahanan layanan eksternal agar sistem dapat bekerja lebih stabil pada skala penggunaan yang lebih luas.

## BAB VI PENUTUP

### 6.1 Simpulan
Berdasarkan analisis kebutuhan (Bab III), perancangan sistem (Bab IV), serta implementasi dan pengujian (Bab V), dapat disimpulkan bahwa:
1. Permasalahan utama pada sistem sebelumnya, yaitu pemantauan ulasan yang masih manual dan tidak terstruktur, telah terpecahkan melalui sistem monitoring berbasis web yang melakukan pengambilan data ulasan secara otomatis dan berkala.
2. Tujuan penelitian untuk membangun sistem analisis sentimen ulasan hotel berhasil dicapai. Sistem mampu mengklasifikasikan ulasan ke dalam kategori POSITIF dan NEGATIF menggunakan model Naive Bayes dan SVM, kemudian menampilkan hasilnya pada dashboard monitoring.
3. Rumusan masalah terkait pemilihan model terbaik telah terjawab secara objektif berdasarkan hasil evaluasi. Model terbaik yang dipilih dalam penelitian ini adalah Support Vector Machine pada skenario balance karena memberikan akurasi tertinggi sebesar 0.9540, didukung F1 Macro sebesar 0.8405. Meskipun demikian, SVM pada skenario tidak balance tetap menunjukkan temuan penting karena menghasilkan balanced accuracy tertinggi sebesar 0.8950.
4. Rumusan masalah terkait penyajian informasi analitik juga terjawab, karena sistem telah menyediakan fitur ringkasan sentimen, tren ulasan, rating, keyword, serta notifikasi Telegram untuk mendukung respons pengguna terhadap ulasan baru.
5. Sistem telah berjalan sesuai ruang lingkup penelitian untuk konteks pengguna hotel, dengan karakter layanan near real-time berbasis interval scheduler.

### 6.2 Saran
Beberapa hal yang belum atau masih terbatas pada tugas akhir ini dan dapat dikembangkan pada penelitian berikutnya adalah:
1. Menambahkan anotasi manual pada sebagian data sebagai pembanding agar validitas label meningkat dan bias weak supervision dapat dikurangi.
2. Memperluas sumber dan jumlah dataset (lebih banyak hotel, periode lebih panjang, dan variasi gaya bahasa) untuk meningkatkan generalisasi model.
3. Mengembangkan klasifikasi sentimen multi-kelas (positif, netral, negatif) atau aspect-based sentiment analysis agar insight lebih detail.
4. Menambahkan mekanisme retry, queue, dan monitoring layanan eksternal untuk meningkatkan keandalan integrasi SerpAPI dan Telegram.
5. Melakukan evaluasi lanjutan menggunakan metrik yang lebih lengkap serta validasi silang pada dataset yang lebih beragam agar pemilihan model terbaik menjadi semakin kuat secara metodologis.
6. Mengembangkan fitur analitik lanjutan berbasis rekomendasi tindakan sehingga sistem tidak hanya memantau, tetapi juga membantu prioritas perbaikan layanan.

## Lampiran
- Lampiran A: Struktur Proyek (`APP TA/`)
- Lampiran B: Skema Basis Data (`schema.sql`)
- Lampiran C: Endpoint Halaman dan API (`app.py`)
- Lampiran D: Hasil Evaluasi Model (`analisis/model_machine/*.json`)
- Lampiran E: Screenshot UI (Login, Dashboard, Analytics)

## Daftar Pustaka (Template)
1. [Tambahkan referensi jurnal terkait analisis sentimen]
2. [Tambahkan referensi metode TF-IDF, Naive Bayes, SVM, dan balancing data]
3. [Tambahkan dokumentasi Flask, scikit-learn, APScheduler]
4. [Tambahkan dokumentasi SerpAPI dan Telegram Bot API]
