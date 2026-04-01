## BAB V IMPLEMENTASI, HASIL, DAN PEMBAHASAN

### 5.1 Implementasi Sistem

Bab ini menjelaskan implementasi teknis sistem monitoring sentimen ulasan hotel berbasis web yang dikembangkan pada penelitian ini. Uraian pada bab ini meliputi lingkungan implementasi, arsitektur sistem, implementasi model analisis sentimen, implementasi pipeline monitoring, implementasi antarmuka, hasil pengujian model, serta pembahasan hasil penelitian. Seluruh penjelasan disusun berdasarkan implementasi aktual pada proyek agar konsisten dengan artefak aplikasi, struktur kode, dan hasil eksperimen yang digunakan.

#### 5.1.1 Lingkungan Implementasi

Implementasi sistem dilakukan menggunakan perangkat keras dan perangkat lunak sebagai berikut.

a. Perangkat keras
   - Laptop dengan prosesor AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx
   - RAM 8 GB
   - SSD 256 GB
   - Smartphone Android untuk pengujian notifikasi Telegram

b. Perangkat lunak
   - Sistem operasi Microsoft Windows 11
   - Google Chrome sebagai browser pengujian
   - Visual Studio Code sebagai editor kode
   - Google Colab untuk eksperimen model awal
   - Python sebagai bahasa pemrograman utama
   - Flask sebagai framework backend
   - MySQL/MariaDB sebagai basis data
   - scikit-learn, pandas, joblib, NLTK, dan Sastrawi sebagai library pengolahan data dan machine learning
   - APScheduler untuk penjadwalan monitoring
   - SerpAPI untuk pengambilan data ulasan Google Maps
   - Telegram Bot API untuk pengiriman notifikasi
   - Draw.io untuk penyusunan diagram

Pemilihan perangkat dan perangkat lunak tersebut didasarkan pada kebutuhan penelitian yang mencakup pengembangan aplikasi web, pengolahan data teks, penyimpanan data terstruktur, serta integrasi layanan eksternal untuk monitoring ulasan secara berkala.

#### 5.1.2 Implementasi Arsitektur Sistem

Sistem dibangun menggunakan pendekatan arsitektur aplikasi web berbasis Flask dengan pemisahan tanggung jawab antar komponen. Lapisan presentasi diimplementasikan menggunakan template HTML, CSS, JavaScript, Bootstrap, dan Jinja, sedangkan lapisan logika aplikasi dikelola melalui `app.py`. Proses scraping, prediksi sentimen, pengelolaan notifikasi, dan koneksi basis data ditempatkan pada folder `pipeline/` agar struktur aplikasi tetap modular dan mudah dipelihara.

Gambar 5.1 Implementasi Arsitektur Sistem Monitoring Sentimen

Secara umum, alur implementasi sistem adalah sebagai berikut.

1. Pengguna melakukan autentikasi ke dalam sistem.
2. Sistem menentukan hotel aktif yang terhubung dengan akun pengguna.
3. Scheduler atau pengguna memicu proses scraping ulasan terbaru.
4. Sistem mengambil ulasan terbaru dari Google Maps melalui SerpAPI.
5. Ulasan yang diperoleh dinormalisasi, dicek duplikasi, lalu diprediksi sentimennya menggunakan model Naive Bayes dan SVM.
6. Hasil prediksi disimpan ke dalam basis data.
7. Dashboard dan halaman analitik menampilkan hasil secara dinamis.
8. Jika terdapat subscriber Telegram, sistem mengirim notifikasi otomatis dan menyimpan log pengiriman.

Pada Gambar 5.1 terlihat bahwa implementasi arsitektur sistem dimulai dari interaksi pengguna melalui browser web pada lapisan presentasi. Permintaan dari pengguna diteruskan ke `app.py` sebagai pusat logika aplikasi, kemudian diproses bersama scheduler dan modul-modul pada folder `pipeline/`. Selanjutnya, sistem berinteraksi dengan SerpAPI untuk mengambil ulasan terbaru, model machine learning untuk melakukan klasifikasi sentimen, basis data untuk menyimpan hasil pemrosesan, dan Telegram Bot API untuk mengirimkan notifikasi. Hasil akhir dari seluruh proses tersebut ditampilkan kembali pada dashboard, halaman analitik, halaman riwayat ulasan, serta modul administrasi data sebagai antarmuka monitoring dan pengelolaan sistem.

Arsitektur ini menunjukkan bahwa sistem tidak hanya berfungsi sebagai alat klasifikasi sentimen, tetapi juga sebagai platform monitoring operasional yang terintegrasi dari akuisisi data hingga distribusi informasi.

#### 5.1.3 Implementasi Model Analisis Sentimen

Implementasi model analisis sentimen pada penelitian ini dilakukan dengan mengklasifikasikan ulasan Google Maps ke dalam kategori sentimen menggunakan pendekatan machine learning. Data yang telah dikumpulkan dan diberi label terlebih dahulu melalui tahap preprocessing untuk membersihkan dan menormalkan teks, kemudian dibagi menjadi data pelatihan dan pengujian dengan rasio 80:20. Representasi fitur dilakukan menggunakan metode TF-IDF untuk mengubah teks menjadi vektor numerik. Selanjutnya, model Naive Bayes dan Support Vector Machine (SVM) dilatih menggunakan data pelatihan dan dievaluasi menggunakan beberapa metrik untuk menentukan model terbaik sebelum diintegrasikan ke dalam sistem monitoring sentimen.

##### 5.1.3.1 Pengumpulan Data Historis

Pada penelitian ini, proses pengumpulan data historis ulasan dilakukan melalui teknik *web scraping* pada platform Google Maps dengan memanfaatkan skrip JavaScript yang dijalankan melalui browser. Pada tahap eksperimen dataset, scraping dilakukan untuk memperoleh kumpulan ulasan historis yang selanjutnya digunakan sebagai dataset analisis sentimen. Teknik ini digunakan untuk membangun data pelatihan dan data pengujian model.

Gambar 5.2 Kode Program DOM Scraping Data Historis

Pada Gambar 5.2 ditunjukkan implementasi pengambilan data historis menggunakan pendekatan DOM scraping berbasis browser. Tahap awal dilakukan dengan simulasi *scrolling* otomatis menggunakan fungsi `scrollWindow()`, yang bertujuan untuk memuat ulasan secara dinamis (*lazy loading*). Karena Google Maps menerapkan mekanisme pemuatan bertahap saat pengguna menggulir halaman, proses *scroll* berulang dengan interval waktu tertentu diperlukan agar seluruh ulasan yang tersedia dapat ditampilkan secara maksimal pada *Document Object Model* (DOM).

Setelah seluruh ulasan termuat, proses ekstraksi data dilakukan dengan mengakses elemen HTML berdasarkan *class selector* seperti `.Svr5cf.bKhjM`, `.GDWaad`, dan `.STQFb.eoY5cb .K7oBsc`. Informasi yang diambil pada tahap ini meliputi teks ulasan dan rating, yang kemudian disusun ke dalam struktur data sederhana. Hasil ekstraksi tersebut selanjutnya disimpan ke dalam format JSON agar dapat diproses lebih lanjut pada tahap berikutnya.

Gambar 5.3 Kode Program Konversi Data JSON ke CSV

Setelah proses scraping menghasilkan file berformat JSON, tahap selanjutnya adalah melakukan transformasi data menjadi format CSV (*Comma-Separated Values*) agar lebih mudah diproses pada tahapan analisis menggunakan Python dan library machine learning seperti scikit-learn. Konversi ini dilakukan menggunakan library `pandas`, yang merupakan pustaka utama dalam pengolahan data terstruktur. Dengan demikian, data hasil scraping dapat langsung digunakan pada proses preprocessing, pelabelan, pelatihan model, dan evaluasi.

##### 5.1.3.2 Pelabelan Data

Pada tahap pelabelan data sentimen, penelitian ini memanfaatkan pendekatan otomatis berbasis *pre-trained transformer model* menggunakan library `transformers`. Model yang digunakan adalah `w11wo/indonesian-roberta-base-sentiment-classifier`, yaitu model berbasis arsitektur RoBERTa yang telah dilatih khusus untuk klasifikasi sentimen teks berbahasa Indonesia.

Gambar 5.4 Kode Program Pelabelan Data Menggunakan RoBERTa

Pada Gambar 5.4 dapat dijelaskan bahwa proses dimulai dengan inisialisasi `pipeline` untuk *sentiment-analysis*, yang secara otomatis menangani proses tokenisasi, encoding, dan inferensi model. Parameter `truncation=True` dan `max_length=512` digunakan untuk memastikan teks ulasan yang panjang tetap dapat diproses tanpa melebihi batas maksimum token model. Fungsi pelabelan mengembalikan nilai numerik, yaitu `1` untuk sentimen positif dan `0` untuk sentimen negatif.

Secara metodologis, pelabelan ini termasuk pendekatan *weak supervision* karena label referensi tidak berasal dari anotasi manual penuh oleh manusia. Oleh karena itu, kualitas label tetap memiliki keterbatasan yang perlu dijelaskan secara eksplisit dalam laporan.

##### 5.1.3.3 Preprocessing Data

Tahap preprocessing data dilakukan untuk membersihkan teks ulasan sebelum proses ekstraksi fitur dan pelatihan model. Proses ini meliputi *case folding*, *cleaning*, tokenisasi, normalisasi, *stopword removal*, dan stemming. Tahapan ini bertujuan untuk mengurangi *noise* dan meningkatkan kualitas representasi teks sehingga model klasifikasi sentimen dapat bekerja secara lebih optimal.

1. *Case folding*  
   Pada tahap awal preprocessing, dilakukan proses *case folding*, yaitu mengubah seluruh teks ulasan menjadi huruf kecil (*lowercase*). Tahap ini bertujuan untuk menyeragamkan representasi kata sehingga tidak terjadi perbedaan fitur akibat variasi huruf besar dan kecil.

Gambar 5.5 Kode Program *Case Folding*

2. *Cleaning*  
   Setelah *case folding*, tahap berikutnya adalah *cleaning*, yaitu proses pembersihan teks dari URL, angka, tanda baca, karakter nonhuruf, simbol yang tidak relevan, serta huruf berulang berlebihan. Proses ini juga mencakup normalisasi khusus untuk frasa seperti "bintang 1" sampai "bintang 5" agar tetap terbaca sebagai fitur linguistik.

Gambar 5.6 Kode Program *Cleaning* Teks

3. Tokenisasi  
   Tokenisasi dilakukan untuk memecah teks menjadi unit-unit kata (*tokens*) sehingga data dapat diproses lebih lanjut dalam analisis berbasis fitur.

Gambar 5.7 Kode Program Tokenisasi

4. Normalisasi  
   Tahap normalisasi dilakukan untuk mengubah kata tidak baku, singkatan, atau bahasa slang ke bentuk baku sesuai konteks bahasa Indonesia. Pendekatan yang digunakan adalah *dictionary-based normalization* yang disusun secara manual berdasarkan karakteristik data penelitian.

Gambar 5.8 Kode Program Normalisasi Kata

5. *Stopword removal*  
   Tahap ini bertujuan menghapus kata-kata umum yang tidak memiliki kontribusi signifikan terhadap penentuan sentimen. Daftar stopword dibentuk dari gabungan stopword bahasa Indonesia dari NLTK dan stopword tambahan yang disusun berdasarkan karakteristik dataset.

Gambar 5.9 Kode Program *Stopword Removal*

6. Stemming  
   Tahap akhir preprocessing adalah stemming, yaitu proses mengubah kata berimbuhan menjadi bentuk dasar menggunakan pustaka Sastrawi.

Gambar 5.10 Kode Program Stemming

Melalui rangkaian preprocessing tersebut, data teks menjadi lebih terstruktur dan siap digunakan pada tahap pembentukan fitur dan pelatihan model.

##### 5.1.3.4 Pembagian Data dan Ekstraksi Fitur

Setelah preprocessing selesai, data dibagi menjadi data pelatihan dan data pengujian menggunakan rasio 80:20. Pembagian ini bertujuan untuk mengevaluasi kemampuan generalisasi model terhadap data yang belum pernah dilihat sebelumnya.

Gambar 5.11 Kode Program *Train-Test Split*

Pada Gambar 5.11, pembagian data dilakukan menggunakan `train_test_split` dari scikit-learn dengan `test_size=0.2` dan `random_state=42`. Parameter ini digunakan agar hasil pembagian data konsisten dan dapat direproduksi.

Tahap berikutnya adalah ekstraksi fitur menggunakan metode TF-IDF untuk mengubah data teks hasil preprocessing menjadi representasi numerik. TF-IDF memberikan bobot pada setiap kata berdasarkan frekuensi kemunculannya dalam dokumen dan tingkat keunikannya dalam korpus secara keseluruhan.

Gambar 5.12 Kode Program Ekstraksi Fitur TF-IDF

Pada implementasinya, `TfidfVectorizer` digunakan dengan penyesuaian karena data sudah dalam bentuk token hasil preprocessing. Proses `fit_transform` diterapkan pada data pelatihan, sedangkan data pengujian hanya melewati proses `transform` untuk menghindari *data leakage*. Hasil dari tahap ini berupa matriks fitur numerik yang menjadi masukan bagi model klasifikasi. Pada eksperimen penelitian ini, ukuran kosakata TF-IDF yang terbentuk adalah 5.123 fitur.

##### 5.1.3.5 Penyeimbangan Data Latih

Setelah data latih diubah ke representasi numerik menggunakan TF-IDF, tahap berikutnya adalah penyeimbangan distribusi kelas pada data pelatihan. Tahap ini dilakukan karena jumlah data antar kelas sentimen tidak sepenuhnya seimbang, sehingga berpotensi memengaruhi kemampuan model dalam mempelajari pola dari kelas minoritas. Penyeimbangan hanya diterapkan pada data latih, sedangkan data uji tetap dipertahankan dalam distribusi aslinya agar evaluasi model tetap mencerminkan kondisi data nyata.

```python
from sklearn.utils import resample
import numpy as np

def upsample_minority_sparse(X, y, random_state=42):
    y_arr = np.asarray(y)
    classes, counts = np.unique(y_arr, return_counts=True)
    maj_class = classes[np.argmax(counts)]
    min_class = classes[np.argmin(counts)]

    idx_maj = np.where(y_arr == maj_class)[0]
    idx_min = np.where(y_arr == min_class)[0]
    idx_min_up = resample(idx_min, replace=True, n_samples=len(idx_maj), random_state=random_state)

    idx_bal = np.concatenate([idx_maj, idx_min_up])
    np.random.RandomState(random_state).shuffle(idx_bal)
    return X[idx_bal], y_arr[idx_bal]
```

Gambar 5.13 Kode Program Penyeimbangan Data Latih

Pada Gambar 5.13, penyeimbangan data dilakukan dengan teknik *oversampling* terhadap kelas minoritas menggunakan fungsi `resample` dari scikit-learn. Proses ini memilih kembali sampel dari kelas minoritas secara acak dengan pengembalian (*replace=True*) hingga jumlahnya setara dengan kelas mayoritas. Setelah itu, indeks data hasil penyeimbangan diacak kembali agar susunan data latih tidak bersifat terurut berdasarkan kelas. Dengan pendekatan ini, model diharapkan dapat mempelajari pola kedua kelas secara lebih seimbang.

Melalui tahapan tersebut, penelitian ini memiliki dua skenario eksperimen, yaitu skenario dengan distribusi kelas asli yang tidak seimbang dan skenario dengan penyeimbangan data latih melalui *resampling* pada kelas minoritas. Perbandingan kedua skenario ini digunakan untuk mengevaluasi pengaruh distribusi kelas terhadap performa model Naive Bayes dan Support Vector Machine.

##### 5.1.3.6 Pelatihan dan Evaluasi Model Naive Bayes

Naive Bayes digunakan sebagai salah satu algoritma klasifikasi sentimen karena memiliki komputasi yang cepat, sederhana, dan efektif pada data teks berdimensi tinggi. Pada tahap eksperimen, model dilatih menggunakan pendekatan validasi silang dan optimasi parameter.

Gambar 5.14 Kode Program Pelatihan Model Naive Bayes

Pada Gambar 5.14, pelatihan model dilakukan menggunakan `GridSearchCV` dengan `StratifiedKFold` untuk menjaga proporsi distribusi kelas sentimen pada setiap *fold*. Parameter yang dioptimasi adalah `alpha`, sedangkan metrik evaluasi yang digunakan pada tahap pencarian parameter adalah `F1-score macro`.

Setelah model terbaik diperoleh, tahap selanjutnya adalah evaluasi pada data pengujian untuk mengukur kemampuan generalisasi model terhadap data baru.

Gambar 5.15 Kode Program Pengujian dan Evaluasi Model Naive Bayes

Pada tahap evaluasi, digunakan metrik *accuracy*, *precision weighted*, *recall weighted*, *F1-score weighted*, *F1-score macro*, *balanced accuracy*, serta *log loss*. Selain itu, confusion matrix divisualisasikan untuk memperjelas distribusi prediksi benar dan salah pada masing-masing kelas. Setelah melalui tahap evaluasi, model terbaik disimpan dalam bentuk file `naive_bayes_model.pkl` agar dapat digunakan kembali pada sistem produksi tanpa proses pelatihan ulang.

##### 5.1.3.7 Pelatihan dan Evaluasi Model Support Vector Machine

Model Support Vector Machine (SVM) digunakan untuk membangun *hyperplane* optimal yang memisahkan kelas sentimen positif dan negatif. Pada penelitian ini, SVM dilatih menggunakan kernel linear karena sesuai untuk klasifikasi teks dan efisien secara komputasi.

Gambar 5.16 Kode Program Pelatihan Model Support Vector Machine

Pelatihan model dilakukan menggunakan `LinearSVC` dengan optimasi parameter `C` melalui `GridSearchCV` dan validasi silang `StratifiedKFold`. Pendekatan ini digunakan untuk memperoleh konfigurasi model yang stabil dan representatif terhadap distribusi data.

Gambar 5.17 Kode Program Pengujian dan Evaluasi Model Support Vector Machine

Pada tahap evaluasi, digunakan metrik *accuracy*, *precision weighted*, *recall weighted*, *F1-score weighted*, *F1-score macro*, *balanced accuracy*, serta *hinge loss*. Confusion matrix juga divisualisasikan untuk melihat distribusi hasil prediksi. Setelah model terbaik diperoleh, model disimpan dalam file `SVM_model.pkl` agar dapat langsung digunakan pada tahap implementasi sistem.

#### 5.1.4 Implementasi Pipeline Sentiment Monitoring

Tahap ini menjelaskan implementasi teknis sistem yang memungkinkan proses pengambilan data ulasan, analisis sentimen, penyimpanan hasil, hingga pengiriman notifikasi dilakukan secara otomatis. Pada sistem yang sekarang, pipeline monitoring terhubung langsung dengan aplikasi Flask sehingga dapat dipicu secara manual melalui antarmuka web maupun secara berkala melalui scheduler. Komponen utamanya terdiri atas scheduler, scraping melalui SerpAPI, integrasi model, koneksi basis data, dan pengiriman notifikasi melalui Telegram.

##### 5.1.4.1 Implementasi Scheduler

Scheduler berfungsi sebagai mekanisme otomatisasi untuk menjalankan proses monitoring dalam interval waktu tertentu tanpa intervensi manual. Pada sistem final, scheduler diimplementasikan menggunakan APScheduler dan dijalankan di dalam aplikasi Flask agar dapat menangani job scraping per hotel secara lebih stabil. Pengendalian scheduler dilakukan melalui endpoint aplikasi untuk proses mulai, berhenti, dan pengecekan status job.

Gambar 5.18 Kode Program Scheduler Sistem Monitoring

Pada Gambar 5.18, scheduler bertugas memicu proses scraping dan pipeline monitoring secara berkala sesuai interval yang ditentukan oleh pengguna. Setiap job dijalankan berdasarkan hotel aktif, sehingga proses monitoring tetap terisolasi sesuai lingkup data akun yang sedang digunakan. Melalui mekanisme ini, pengguna dapat menyalakan scheduler, menghentikannya, serta memantau interval dan waktu eksekusi berikutnya dari antarmuka web. Pendekatan tersebut memastikan sistem dapat mendeteksi ulasan baru tanpa perlu menunggu perintah manual dari pengguna. Dari sisi metodologis, karakter layanan yang dihasilkan lebih tepat disebut **near real-time**, karena pembaruan data bergantung pada interval polling scheduler.

##### 5.1.4.2 Implementasi Scraping Menggunakan SerpAPI

Proses pengambilan data ulasan Google Maps pada sistem produksi dilakukan menggunakan layanan API eksternal, yaitu SerpAPI. Pada konteks implementasi aplikasi, modul ini berperan sebagai mekanisme pengambilan data operasional yang memasok ulasan terbaru ke dalam alur monitoring sentimen. Pendekatan ini dipilih karena lebih stabil dibanding scraping berbasis parsing HTML langsung pada halaman Google Maps.

Gambar 5.19 Implementasi Scraping Menggunakan SerpAPI

Pada implementasi ini, sistem mengambil `place_id` hotel dari basis data, kemudian mengirimkannya bersama `API key` ke layanan SerpAPI untuk memperoleh ulasan terbaru dalam format data terstruktur. Data hasil scraping memuat nama pengguna, rating, teks ulasan, dan waktu ulasan. Apabila diperlukan, teks ulasan diterjemahkan terlebih dahulu ke bahasa Indonesia sebelum memasuki tahap klasifikasi. Sistem juga melakukan parsing waktu ulasan dan pengecekan duplikasi berdasarkan hotel, pengguna, teks ulasan, rating, dan sumber data untuk memastikan bahwa hanya ulasan baru yang disimpan ke basis data. Dengan demikian, modul ini tidak hanya berfungsi sebagai komponen scraping, tetapi juga sebagai sumber pengambilan data operasional yang menjaga agar dashboard, halaman riwayat ulasan, halaman analitik, dan notifikasi selalu diperbarui berdasarkan ulasan terbaru.

##### 5.1.4.3 Implementasi Integrasi Model Analisis ke Sistem

Integrasi model klasifikasi dilakukan melalui file `pipeline/model_predict.py` dengan memuat model hasil pelatihan menggunakan library `joblib`. Pada tahap ini, sistem tidak lagi melakukan proses pelatihan ulang, melainkan langsung menggunakan artefak model yang telah dihasilkan pada tahap eksperimen.

```python
import joblib

class ModelPredict:
    def __init__(self):
        self.nb_model = joblib.load("model_ml/naive_bayes_model.pkl")
        self.svm_model = joblib.load("model_ml/SVM_model.pkl")
        self.vectorizer = joblib.load("model_ml/vectorizer.pkl")

    def predict_nb(self, text):
        vec = self.vectorizer.transform([text])
        return "POSITIF" if self.nb_model.predict(vec)[0] == 1 else "NEGATIF"

    def predict_svm(self, text):
        vec = self.vectorizer.transform([text])
        return "POSITIF" if self.svm_model.predict(vec)[0] == 1 else "NEGATIF"
```

Gambar 5.20 Implementasi Integrasi Model Klasifikasi

Pada Gambar 5.20 terlihat bahwa sistem memuat tiga artefak utama, yaitu `naive_bayes_model.pkl`, `SVM_model.pkl`, dan `vectorizer.pkl`. Teks ulasan terlebih dahulu diubah ke representasi numerik menggunakan vectorizer TF-IDF, kemudian diprediksi oleh model Naive Bayes dan Support Vector Machine. Hasil prediksi selanjutnya dinormalisasi ke dalam dua kategori, yaitu `POSITIF` dan `NEGATIF`, sehingga dapat langsung digunakan pada proses penyimpanan data, visualisasi dashboard, dan pengiriman notifikasi.

##### 5.1.4.4 Implementasi Integrasi Basis Data

Integrasi basis data bertujuan menyediakan mekanisme penyimpanan data yang terstruktur, konsisten, dan berkelanjutan terhadap seluruh proses monitoring ulasan. Basis data menjadi komponen sentral yang menghubungkan modul scraping, modul klasifikasi sentimen, dan modul notifikasi.

```python
import os
import mysql.connector

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "monitoring_review"),
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
```

Gambar 5.21 Implementasi Koneksi Basis Data

Pada Gambar 5.21 ditunjukkan bahwa konfigurasi koneksi database disimpan secara terpusat melalui parameter lingkungan, kemudian digunakan oleh modul `mysql_connector.py` untuk membangun koneksi ke MySQL/MariaDB. Modul ini juga menyediakan fungsi-fungsi utama untuk pengelolaan data pengguna, hotel, ulasan, hasil sentimen, subscriber Telegram, dan log notifikasi. Pendekatan modular tersebut memudahkan proses pemeliharaan karena logika akses data dipisahkan dari modul lain.

##### 5.1.4.5 Implementasi Notifikasi Telegram

Integrasi Telegram pada sistem bertujuan menyediakan mekanisme notifikasi otomatis kepada administrator atau pengguna yang telah berlangganan ketika sistem mendeteksi ulasan baru beserta hasil analisis sentimennya. Pada implementasi aktual, integrasi ini mencakup dua fungsi, yaitu bot untuk proses subscribe dan kanal pengiriman pesan otomatis untuk hasil monitoring.

```python
import requests
import config
from pipeline.mysql_connector import get_subscribers

def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    return requests.post(url, data=payload, timeout=12).status_code == 200

def broadcast_telegram(hotel_id, review_text, sentiment_nb, sentiment_svm, rating=None, user="System"):
    subscribers = get_subscribers(hotel_id)
    for sub in subscribers:
        message = (
            f"<b>Review Baru</b>\n"
            f"<b>User:</b> {user}\n"
            f"<b>Rating:</b> {rating}\n"
            f"<b>Review:</b> {(review_text or '-')[:400]}\n"
            f"<b>Naive Bayes:</b> {sentiment_nb}\n"
            f"<b>Support Vector Machine:</b> {sentiment_svm}"
        )
        send_message(sub["chat_id"], message)
```

Gambar 5.22 Implementasi Telegram Bot Notifikasi

Pada Gambar 5.22 terlihat bahwa sistem mengambil `chat_id` subscriber yang aktif dari tabel `telegram_users`, kemudian menyusun pesan yang memuat nama pengguna, rating, cuplikan ulasan, hasil prediksi Naive Bayes, hasil prediksi SVM, dan waktu ulasan. Selain itu, bot Telegram juga mendukung proses pendaftaran subscriber melalui perintah `/start <hotel_id>` agar akun Telegram dapat dikaitkan dengan hotel tertentu. Setiap pengiriman pesan dicatat ke dalam tabel `notifications` sebagai log distribusi notifikasi.

#### 5.1.5 Implementasi Antarmuka Sistem

Tahap implementasi antarmuka sistem dilakukan untuk menerjemahkan hasil analisis dan proses klasifikasi sentimen ke dalam bentuk visual yang informatif, interaktif, serta mudah dipahami oleh pengguna. Sistem dirancang berbasis web agar dapat diakses secara fleksibel melalui berbagai perangkat, serta mampu menampilkan hasil klasifikasi sentimen, tren waktu, dan notifikasi secara dinamis. Implementasi ini mengintegrasikan model klasifikasi yang telah melalui proses pelatihan, optimasi, dan evaluasi pada tahap sebelumnya, sehingga sistem yang dibangun tidak hanya bersifat operasional, tetapi juga memiliki dasar metodologis yang dapat dipertanggungjawabkan secara ilmiah.

Pengembangan antarmuka dilakukan menggunakan framework Flask sebagai penghubung antara backend dan frontend. Backend bertugas menangani proses inferensi terhadap data ulasan yang masuk, pengambilan data dari basis data, serta penyimpanan hasil klasifikasi dan aktivitas sistem. Sementara itu, frontend berperan sebagai lapisan presentasi yang menampilkan hasil pengolahan data dalam bentuk dashboard visual, grafik tren sentimen berdasarkan waktu, riwayat ulasan, pengelolaan subscriber, dan log notifikasi. Dengan pemisahan peran yang jelas antara backend dan frontend, sistem mampu menjaga efisiensi proses komputasi sekaligus memberikan pengalaman pengguna yang informatif dan terstruktur. Pada implementasi aktual, antarmuka juga dibedakan berdasarkan peran pengguna, yaitu area pengguna untuk aktivitas monitoring dan area admin untuk pengelolaan hotel, akun, serta data inti sistem.

Secara teknis, seluruh halaman antarmuka pada sistem dibangun menggunakan mekanisme *template inheritance* dari Jinja. File `base.html` berfungsi sebagai kerangka utama yang memuat struktur layout umum, seperti navigasi, pemanggilan aset CSS dan JavaScript, serta blok konten yang digunakan kembali oleh halaman login, register, dashboard, analitik, subscriber, notifikasi, dan riwayat ulasan. Dengan pendekatan ini, tampilan antarmuka menjadi lebih konsisten, modular, dan mudah dipelihara, sehingga perubahan pada layout umum tidak perlu dilakukan berulang pada setiap file halaman.

Dalam penulisan laporan tugas akhir, bagian implementasi antarmuka tidak perlu menampilkan seluruh isi file HTML, CSS, JavaScript, maupun seluruh route pada backend secara lengkap. Yang ditampilkan cukup potongan kode representatif yang menunjukkan alur data utama antara frontend dan backend, sedangkan detail tampilan dijelaskan melalui narasi dan gambar antarmuka. Oleh karena itu, pada subbagian ini hanya disajikan halaman-halaman inti yang paling merepresentasikan fungsi sistem, yaitu login, register, dashboard, analitik, subscriber, notifikasi, dan riwayat ulasan. Sementara itu, halaman administrasi data tidak ditampilkan sebagai subgambar tersendiri karena lebih bersifat pendukung pengelolaan sistem daripada fitur utama monitoring bagi pengguna akhir.

Melalui integrasi antara model machine learning, basis data, dan framework web, sistem monitoring yang dibangun mampu mengolah, menganalisis, dan menyajikan informasi sentimen secara berkelanjutan. Pendekatan ini memastikan bahwa hasil penelitian tidak hanya berhenti pada tahap eksperimen, tetapi dapat diimplementasikan secara nyata dalam bentuk sistem yang fungsional, terstruktur, dan siap digunakan.

##### 5.1.5.1 Implementasi Halaman Login

Halaman login berfungsi sebagai gerbang autentikasi untuk memastikan bahwa hanya pengguna yang memiliki akun terdaftar yang dapat mengakses sistem monitoring sentimen. Dari sisi tampilan, halaman ini memuat form sederhana untuk memasukkan username dan password, serta menampilkan pesan kesalahan apabila autentikasi gagal. Pada laporan, yang ditampilkan cukup potongan route backend karena bagian ini lebih merepresentasikan logika autentikasi daripada detail tampilan HTML.

```python
@app.get("/login")
def login():
    if "uid" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.post("/login")
def login_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = db.get_user_by_username(username)

    if not user or not check_password_hash(user["password"], password):
        return render_template("login.html", error="Username atau password salah")

    if not user.get("hotel_id"):
        return render_template("login.html", error="Akun tidak terhubung ke hotel.")

    session["uid"] = user["user_id"]
    session["uname"] = user["username"]
    session["hotel_id"] = int(user["hotel_id"])
    session["active_hotel_id"] = session["hotel_id"]
    session["role"] = user.get("role") or "user"

    if (session["role"] or "").lower() == "admin":
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("dashboard"))
```

Gambar 5.23 Implementasi Halaman Login

Pada Gambar 5.23 terlihat bahwa proses login tidak hanya melakukan validasi username dan password, tetapi juga memastikan bahwa akun terhubung dengan hotel tertentu. Setelah autentikasi berhasil, sistem menyimpan informasi pengguna ke dalam session dan mengarahkan pengguna ke halaman yang sesuai dengan perannya, yaitu area monitoring untuk pengguna biasa dan area administrasi untuk admin.

##### 5.1.5.2 Implementasi Halaman Register

Halaman register digunakan untuk membuat akun baru sekaligus mendaftarkan hotel yang akan dipantau dalam sistem. Dari sisi tampilan, halaman ini menyediakan form untuk username, password, nama hotel, alamat, dan `place_id` atau tautan Google Maps hotel. Pendekatan ini menunjukkan bahwa proses registrasi pada sistem tidak hanya membuat akun pengguna, tetapi juga langsung mengaitkannya dengan objek monitoring.

```python
@app.get("/register")
def register():
    return render_template("register.html")

@app.post("/register")
def register_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    hotel_name = request.form.get("hotel_name", "").strip()
    address = request.form.get("address", "").strip()
    place_id_input = request.form.get("place_id", "").strip()

    place_id = extract_place_id(place_id_input, resolve_redirect=True)
    pw_hash = generate_password_hash(password)
    db.create_hotel_and_user(username, pw_hash, hotel_name, address or None, place_id, role="user")
    return redirect(url_for("login"))
```

Gambar 5.24 Implementasi Halaman Register

Pada Gambar 5.24 terlihat bahwa proses registrasi mencakup pembentukan akun pengguna dan pencatatan data hotel secara terintegrasi. Sistem mengekstraksi `place_id` dari input pengguna, kemudian menyimpannya bersama data hotel dan akun baru. Dengan demikian, setelah registrasi selesai, akun pengguna telah siap digunakan untuk memantau ulasan hotel yang bersangkutan.

##### 5.1.5.3 Implementasi Halaman Dashboard

Dashboard merupakan halaman utama dalam sistem monitoring sentimen yang berfungsi menampilkan ringkasan hasil analisis sentimen secara *near real-time* dalam bentuk visual yang interaktif. Dari sisi tampilan, dashboard memuat kartu informasi hotel, ulasan terbaru, distribusi sentimen, tren review, analisis kata kunci, serta kontrol scheduler otomatis. Pada laporan, potongan kode yang ditampilkan cukup berupa route backend yang menyiapkan data utama ke template.

```python
@app.get("/dashboard")
@user_required
def dashboard():
    hotel_id = get_active_hotel_id()
    hotel = db.get_hotel(hotel_id)
    latest = db.get_latest_reviews(hotel_id, limit=1)
    counts = db.count_sentiments(hotel_id)
    trend = db.trend_reviews(hotel_id, days=7)
    avg_rating = db.get_average_rating(hotel_id)
    rating_dist = db.get_rating_distribution(hotel_id)
    weekly = db.get_weekly_comparison(hotel_id)
    keywords = db.get_top_keywords(hotel_id, limit=5)
    return render_template(
        "dashboard.html",
        hotel=hotel,
        latest=latest,
        counts=counts,
        trend=trend,
        avg_rating=avg_rating,
        rating_dist=rating_dist,
        weekly=weekly,
        keywords=keywords,
    )
```

Gambar 5.25 Implementasi Halaman Dashboard

Pada Gambar 5.25 terlihat bahwa dashboard menampilkan informasi utama seperti data hotel aktif, jumlah review, perbandingan sentimen positif dan negatif, rating rata-rata, distribusi rating, ulasan terbaru, dan kontrol scheduler otomatis. Halaman ini menjadi pusat monitoring karena menyajikan informasi paling penting dalam satu tampilan, sekaligus memastikan bahwa data yang ditampilkan sesuai dengan hotel yang terhubung pada akun pengguna.

##### 5.1.5.4 Implementasi Halaman Analitik

Halaman analitik dirancang untuk menyajikan ringkasan statistik dan tren sentimen pelanggan secara komprehensif dalam bentuk visual yang informatif dan interaktif. Dari sisi tampilan, halaman ini menampilkan statistik total sentimen, rata-rata rating, distribusi sentimen, serta tren ulasan harian. Pada laporan, potongan kode yang layak dimasukkan cukup berupa endpoint API yang menyuplai data visualisasi.

```python
@app.get("/api/analytics/sentiment")
@user_required
def api_analytics_sentiment():
    data = db.count_sentiments(get_active_hotel_id())
    return jsonify([{"label": k, "value": v} for k, v in data.items()])

@app.get("/api/analytics/trend")
@user_required
def api_analytics_trend():
    rows = db.get_trend_sentiment(get_active_hotel_id(), days=30)
    return jsonify(rows)
```

Gambar 5.26 Implementasi Halaman Analitik

Pada Gambar 5.26 terlihat bahwa sistem menampilkan visualisasi distribusi sentimen dan tren ulasan harian. Keberadaan halaman ini membantu pengguna memahami pola sentimen secara temporal tanpa harus menelaah seluruh data ulasan satu per satu.

##### 5.1.5.5 Implementasi Halaman Subscriber

Halaman subscriber berfungsi untuk mengelola daftar pengguna Telegram yang terhubung dengan sistem notifikasi berbasis Telegram Bot. Dari sisi tampilan, halaman ini memuat formulir penambahan subscriber, daftar subscriber aktif, serta kontrol untuk menyalakan atau menghentikan bot Telegram. Dalam laporan, bagian yang ditampilkan cukup berupa route utama untuk menambah subscriber dan menampilkan daftar subscriber.

```python
@app.get("/subscribers")
@user_required
def subscribers_page():
    subs = db.get_subscribers(get_active_hotel_id())
    return render_template("subscribers.html", subs=subs)

@app.post("/subscribers")
@user_required
def subscribers_add():
    chat_id = request.form.get("chat_id")
    if chat_id:
        db.add_subscriber(int(chat_id), get_active_hotel_id())
    return redirect(url_for("subscribers_page"))
```

Gambar 5.27 Implementasi Halaman Subscriber

Pada Gambar 5.27 terlihat bahwa pengguna dapat menambahkan `chat_id`, menghapus subscriber, serta mengontrol bot Telegram melalui antarmuka web. Fitur ini mendukung distribusi informasi yang lebih efisien kepada pihak-pihak yang berkepentingan.

##### 5.1.5.6 Implementasi Halaman Notifikasi

Halaman notifikasi berfungsi menampilkan riwayat pengiriman notifikasi otomatis kepada subscriber melalui Telegram Bot. Dari sisi tampilan, halaman ini menyajikan tabel log notifikasi yang dapat dicari dan dibatasi jumlah tampilannya. Potongan kode yang perlu ditampilkan cukup berupa route halaman dan endpoint backend yang menyediakan data notifikasi secara dinamis.

```python
@app.get("/notifications")
@user_required
def notifications_page():
    rows = db.get_notifications(get_active_hotel_id(), limit=100)
    return render_template("notifications.html", rows=rows)

@app.get("/api/notifications")
@user_required
def get_notifications():
    rows = db.get_notifications(get_active_hotel_id(), limit=150)
    return jsonify(rows)
```

Gambar 5.28 Implementasi Halaman Notifikasi

Pada Gambar 5.28 terlihat bahwa sistem mencatat `review_id`, `chat_id`, status pengiriman, dan waktu pengiriman notifikasi. Halaman ini berperan penting sebagai mekanisme audit dan kontrol distribusi informasi.

##### 5.1.5.7 Implementasi Halaman Riwayat Ulasan

Halaman riwayat ulasan berfungsi menampilkan riwayat ulasan yang telah diproses oleh sistem klasifikasi sentimen. Halaman ini memungkinkan pengguna meninjau data ulasan pelanggan beserta hasil prediksi Naive Bayes dan SVM. Dari sisi tampilan, halaman ini disusun dalam bentuk tabel interaktif yang mendukung pencarian, pembatasan jumlah data, dan ekspor hasil. Pada laporan, potongan kode yang ditampilkan cukup merepresentasikan route backend untuk mengambil data hasil klasifikasi.

```python
@app.get("/reviews")
@user_required
def reviews_page():
    rows = db.list_sentiments(get_active_hotel_id(), limit=100)
    return render_template("reviews.html", rows=rows)

@app.get("/api/reviews")
@user_required
def api_reviews():
    rows = db.list_sentiments(get_active_hotel_id(), limit=100)
    return jsonify(rows)
```

Gambar 5.29 Implementasi Halaman Riwayat Ulasan

Pada Gambar 5.29 terlihat bahwa sistem menyajikan riwayat ulasan dalam bentuk tabel yang memuat waktu ulasan, nama pengguna, rating, teks ulasan, serta hasil prediksi kedua model. Fitur ini memberikan transparansi terhadap hasil klasifikasi karena pengguna dapat menelusuri kembali data mentah dan hasil prediksinya.

### 5.2 Hasil

#### 5.2.1 Hasil Pengumpulan Data Ulasan

Tahap pengumpulan data menghasilkan dataset historis ulasan hotel dari Google Maps yang digunakan sebagai dasar eksperimen model analisis sentimen. Pada penelitian ini, data diperoleh dari hasil scraping historis dan kemudian disusun menjadi dataset terstruktur untuk kebutuhan pelabelan, preprocessing, pelatihan, dan pengujian model. Secara keseluruhan, jumlah data yang berhasil dikumpulkan adalah 2.449 ulasan.

Hasil pengumpulan data ini menunjukkan bahwa sistem dan tahapan penelitian telah mampu memperoleh data ulasan dalam jumlah yang memadai untuk dilakukan analisis sentimen. Selain memuat teks ulasan, dataset juga memuat informasi pendukung seperti nama pengguna, rating, waktu ulasan, dan sumber data. Keberadaan atribut tersebut penting karena tidak hanya mendukung eksperimen klasifikasi, tetapi juga memungkinkan hasil penelitian diintegrasikan ke dalam sistem monitoring operasional.

Dari sisi penelitian, tahap pengumpulan data menjadi fondasi utama karena kualitas dan kelengkapan dataset sangat memengaruhi proses pelabelan, preprocessing, dan performa model yang dihasilkan. Dengan tersedianya data historis tersebut, penelitian dapat dilanjutkan ke tahap pengolahan teks dan eksperimen model secara lebih terstruktur.

#### 5.2.2 Hasil Pelabelan Data

Setelah data ulasan berhasil dikumpulkan, penelitian dilanjutkan ke tahap pelabelan data sentimen. Pelabelan dilakukan secara otomatis menggunakan model *pre-trained transformer* berbahasa Indonesia untuk mengelompokkan ulasan ke dalam dua kategori, yaitu sentimen positif dan sentimen negatif. Hasil pelabelan ini menjadi dasar pembentukan dataset terlabel yang selanjutnya digunakan pada proses preprocessing, pelatihan, dan pengujian model klasifikasi.

Hasil pelabelan menunjukkan bahwa data ulasan berhasil dikonversi dari bentuk teks mentah menjadi dataset yang memiliki target kelas untuk kebutuhan *supervised learning*. Dari total 2.449 ulasan, diperoleh 1.992 ulasan berlabel positif dan 187 ulasan berlabel negatif. Distribusi ini menunjukkan bahwa dataset penelitian cenderung didominasi oleh sentimen positif, sehingga isu ketidakseimbangan kelas menjadi hal yang perlu diperhatikan pada tahap eksperimen model. Dengan tersedianya label sentimen, proses eksperimen dapat dilanjutkan ke tahap preprocessing, ekstraksi fitur, penyeimbangan data latih, serta evaluasi performa model.

Visualisasi distribusi label setelah proses pembersihan data juga memperlihatkan bahwa dataset didominasi oleh sentimen positif sebesar 89,94%, sedangkan sentimen negatif hanya sebesar 10,06%. Perbedaan proporsi ini menunjukkan adanya ketidakseimbangan kelas yang cukup signifikan. Kondisi tersebut berpotensi menyebabkan model lebih banyak mempelajari pola dari kelas mayoritas, sehingga performa klasifikasi pada kelas minoritas perlu diperhatikan secara khusus. Oleh karena itu, pada tahap eksperimen penelitian ini dilakukan perbandingan antara skenario menggunakan distribusi kelas asli yang tidak seimbang dan skenario penyeimbangan data latih melalui *resampling* kelas minoritas. Ketidakseimbangan kelas tersebut juga menjadi alasan pentingnya penggunaan metrik evaluasi seperti *F1 Macro* dan *balanced accuracy*, karena nilai *accuracy* saja belum cukup untuk menggambarkan kemampuan model dalam mengenali seluruh kelas secara seimbang.

Secara metodologis, hasil pelabelan juga menunjukkan bahwa penelitian telah berhasil membangun dataset yang tidak hanya siap dianalisis secara statistik, tetapi juga siap digunakan pada eksperimen klasifikasi teks. Dengan demikian, pelabelan data berfungsi sebagai penghubung utama antara proses pengumpulan data ulasan dan tahap pembentukan model analisis sentimen.

#### 5.2.3 Hasil Preprocessing Data

Setelah data ulasan berhasil melalui tahap pelabelan sentimen, proses selanjutnya adalah *preprocessing* data. Tahap ini bertujuan untuk membersihkan, menyederhanakan, dan menyeragamkan teks ulasan agar dapat digunakan secara optimal pada proses ekstraksi fitur dan pelatihan model klasifikasi. Dalam penelitian ini, tahapan *preprocessing* yang diterapkan meliputi *case folding*, *cleaning*, tokenisasi, normalisasi, *stopword removal*, dan stemming. Hasil akhir dari rangkaian proses tersebut adalah data teks yang lebih terstruktur, lebih konsisten, dan siap diubah ke dalam representasi numerik menggunakan metode TF-IDF.

Secara umum, hasil *preprocessing* menunjukkan bahwa teks ulasan yang pada awalnya masih mengandung variasi huruf besar dan kecil, tanda baca, angka, kata tidak baku, serta kata-kata umum yang kurang informatif berhasil diubah menjadi token-token yang lebih bersih dan lebih relevan. Kondisi ini penting karena data ulasan hasil *scraping* umumnya masih mengandung banyak *noise* yang dapat mengganggu proses pembelajaran model. Melalui *preprocessing*, unsur-unsur yang tidak memiliki kontribusi besar terhadap analisis sentimen dapat dikurangi, sehingga model klasifikasi memiliki peluang yang lebih baik untuk mempelajari pola sentimen dari kata-kata yang benar-benar bermakna.

Tahap *case folding* dilakukan dengan mengubah seluruh huruf pada teks ulasan menjadi huruf kecil. Proses ini bertujuan untuk menyeragamkan bentuk penulisan kata sehingga sistem tidak menganggap kata yang sama sebagai fitur yang berbeda hanya karena perbedaan kapitalisasi. Sebagai contoh, kata "Hotel", "hotel", dan "HOTEL" akan diperlakukan sebagai satu bentuk kata yang sama, yaitu "hotel". Dengan demikian, jumlah variasi kata yang tidak perlu dapat ditekan sejak awal.

Setelah itu, tahap *cleaning* dilakukan untuk menghapus unsur-unsur yang tidak relevan, seperti tanda baca, angka, simbol, dan karakter khusus lainnya. Proses ini membuat teks menjadi lebih bersih dan memudahkan tahap pemrosesan selanjutnya. Pada data ulasan Google Maps, tahap ini sangat penting karena banyak ulasan ditulis secara informal, sering disertai simbol, angka penilaian, atau tanda baca berulang yang tidak memberikan kontribusi langsung terhadap makna sentimen.

Tahap berikutnya adalah tokenisasi, yaitu proses memecah kalimat menjadi satuan-satuan kata atau token. Melalui tokenisasi, teks yang semula berupa kalimat utuh diubah menjadi daftar kata yang dapat diproses lebih lanjut oleh sistem. Tahap ini menjadi dasar bagi proses normalisasi, penghapusan *stopword*, dan stemming, karena seluruh proses lanjutan bekerja pada level kata.

Normalisasi dilakukan untuk menyeragamkan kata-kata tidak baku, singkatan, atau bentuk penulisan informal menjadi bentuk yang lebih standar. Tahap ini penting mengingat ulasan pengguna pada Google Maps sering menggunakan bahasa sehari-hari, singkatan, atau ejaan yang tidak konsisten. Dengan adanya normalisasi, variasi kata yang sebenarnya memiliki makna sama dapat disatukan ke dalam bentuk yang lebih seragam. Hal ini membantu meningkatkan kualitas representasi fitur dan mengurangi redundansi pada kosakata.

Tahap *stopword removal* dilakukan untuk menghapus kata-kata umum yang frekuensinya tinggi tetapi kontribusinya rendah terhadap penentuan sentimen. Kata-kata seperti kata hubung, kata depan, atau kata umum lainnya biasanya tidak memiliki informasi sentimen yang kuat. Dengan menghapus kata-kata tersebut, sistem dapat lebih fokus pada kata-kata yang mengandung muatan opini, seperti "nyaman", "ramah", "bagus", "kurang", "padam", atau "memuaskan". Oleh karena itu, tahap ini berperan penting dalam meningkatkan efektivitas fitur yang akan digunakan pada proses klasifikasi.

Tahap terakhir adalah stemming, yaitu proses mengubah kata berimbuhan menjadi bentuk dasarnya. Misalnya, kata "membantu" diubah menjadi "bantu", "pelayanan" menjadi "layan", dan "membutuhkan" menjadi "butuh". Dengan stemming, variasi morfologis dari kata yang sama dapat dikurangi sehingga fitur teks menjadi lebih ringkas. Hal ini membantu sistem dalam mengenali pola kata yang serupa meskipun muncul dalam bentuk imbuhan yang berbeda.

Hasil keseluruhan dari tahapan *preprocessing* menunjukkan bahwa data teks yang awalnya panjang dan belum terstruktur dapat diubah menjadi token-token yang lebih singkat, seragam, dan informatif. Tahap ini tidak hanya berfungsi sebagai pembersihan data, tetapi juga sebagai upaya untuk meningkatkan kualitas fitur sebelum data masuk ke tahap ekstraksi fitur dan pemodelan. Dengan kata lain, *preprocessing* merupakan jembatan penting antara data mentah hasil *scraping* dan data siap olah yang digunakan pada proses klasifikasi sentimen.

Contoh hasil *preprocessing* pada beberapa data ulasan dapat dilihat pada Tabel 5.1. Tabel tersebut menunjukkan perubahan bertahap dari teks ulasan asli hingga menjadi token hasil stemming. Melalui contoh tersebut dapat dilihat bahwa setiap tahapan memberikan kontribusi berbeda dalam menyederhanakan teks. *Case folding* dan *cleaning* berperan dalam membersihkan bentuk teks, tokenisasi memecah teks menjadi unit kata, normalisasi menyeragamkan bentuk kata, *stopword removal* menyaring kata yang kurang penting, dan stemming menghasilkan bentuk kata dasar yang lebih ringkas.

Tabel 5.1 Contoh Hasil Preprocessing Data Ulasan

| Loc | Proses | Hasil |
|---|---|---|
| 20 | 1) Teks Ulasan | Strategis sekali, keluar hotel langsung di Jalan Malioboro. Hotelnya nyaman, staf resepsionisnya ramah, sangat membantu, terima kasih Danisha. |
|  | 2) *Case Folding* | strategis sekali, keluar hotel langsung di jalan malioboro. hotelnya nyaman, staf resepsionisnya ramah, sangat membantu, terima kasih danisha. |
|  | 3) *Cleaning* | strategis sekali keluar hotel langsung di jalan malioboro hotelnya nyaman staf resepsionisnya ramah sangat membantu terima kasih danisha |
|  | 4) Tokenisasi | `['strategis', 'sekali', 'keluar', 'hotel', 'langsung', 'di', 'jalan', 'malioboro', 'hotelnya', 'nyaman', 'staf', 'resepsionisnya', 'ramah', 'sangat', 'membantu', 'terima', 'kasih', 'danisha']` |
|  | 5) Normalisasi | `['strategis', 'sekali', 'keluar', 'hotel', 'langsung', 'di', 'jalan', 'malioboro', 'hotelnya', 'nyaman', 'staf', 'resepsionisnya', 'ramah', 'sangat', 'membantu', 'terima', 'kasih', 'danisha']` |
|  | 6) *Stopword Removal* | `['strategis', 'keluar', 'hotel', 'langsung', 'jalan', 'malioboro', 'hotelnya', 'nyaman', 'staf', 'resepsionisnya', 'ramah', 'membantu', 'terima', 'kasih', 'danisha']` |
|  | 7) Stemming | `['strategis', 'keluar', 'hotel', 'langsung', 'jalan', 'malioboro', 'hotel', 'nyaman', 'staf', 'resepsionisnya', 'ramah', 'bantu', 'terima', 'kasih', 'danisha']` |
| 21 | 1) Teks Ulasan | Hotelnya bagus, nyaman. Lokasi strategis, kalau mau ke Malioboro tinggal melangkah buka pintunya, sangat recomended... |
|  | 2) *Case Folding* | hotelnya bagus, nyaman. lokasi strategis, kalau mau ke malioboro tinggal melangkah buka pintunya, sangat recomended... |
|  | 3) *Cleaning* | hotelnya bagus nyaman lokasi strategis kalau mau ke malioboro tinggal melangkah buka pintunya sangat recomended |
|  | 4) Tokenisasi | `['hotelnya', 'bagus', 'nyaman', 'lokasi', 'strategis', 'kalau', 'mau', 'ke', 'malioboro', 'tinggal', 'melangkah', 'buka', 'pintunya', 'sangat', 'recomended']` |
|  | 5) Normalisasi | `['hotelnya', 'bagus', 'nyaman', 'lokasi', 'strategis', 'kalau', 'mau', 'ke', 'malioboro', 'tinggal', 'melangkah', 'buka', 'pintunya', 'sangat', 'rekomendasi']` |
|  | 6) *Stopword Removal* | `['hotelnya', 'bagus', 'nyaman', 'lokasi', 'strategis', 'malioboro', 'tinggal', 'melangkah', 'buka', 'pintunya', 'rekomendasi']` |
|  | 7) Stemming | `['hotel', 'bagus', 'nyaman', 'lokasi', 'strategis', 'malioboro', 'tinggal', 'langkah', 'buka', 'pintu', 'rekomendasi']` |
| 22 | 1) Teks Ulasan | Listrik padam sampai 20 menit, tidak ada penjelasan dari pihak hotel, pelayanan kurang memuaskan. |
|  | 2) *Case Folding* | listrik padam sampai 20 menit, tidak ada penjelasan dari pihak hotel, pelayanan kurang memuaskan. |
|  | 3) *Cleaning* | listrik padam sampai menit tidak ada penjelasan dari pihak hotel pelayanan kurang memuaskan |
|  | 4) Tokenisasi | `['listrik', 'padam', 'sampai', 'menit', 'tidak', 'ada', 'penjelasan', 'dari', 'pihak', 'hotel', 'pelayanan', 'kurang', 'memuaskan']` |
|  | 5) Normalisasi | `['listrik', 'padam', 'sampai', 'menit', 'tidak', 'ada', 'penjelasan', 'dari', 'pihak', 'hotel', 'pelayanan', 'kurang', 'memuaskan']` |
|  | 6) *Stopword Removal* | `['listrik', 'padam', 'menit', 'tidak', 'penjelasan', 'hotel', 'pelayanan', 'kurang', 'memuaskan']` |
|  | 7) Stemming | `['listrik', 'padam', 'menit', 'tidak', 'jelas', 'hotel', 'layan', 'kurang', 'puas']` |

Berdasarkan Tabel 5.1, dapat disimpulkan bahwa proses *preprocessing* berhasil mengurangi kompleksitas teks ulasan tanpa menghilangkan inti informasi yang terkandung di dalamnya. Kata-kata yang dipertahankan pada tahap akhir umumnya merupakan kata-kata yang lebih representatif terhadap opini pengguna. Kondisi ini sangat mendukung proses pembentukan fitur TF-IDF, karena fitur yang dihasilkan menjadi lebih fokus pada kata-kata yang memiliki kontribusi terhadap klasifikasi sentimen. Dengan demikian, tahap *preprocessing* memberikan pengaruh yang signifikan terhadap kualitas data masukan dan berpotensi meningkatkan performa model analisis sentimen yang dibangun pada penelitian ini.

#### 5.2.4 Hasil Pengujian Model Analisis Sentimen

Setelah melalui tahap pelabelan dan *preprocessing*, data ulasan diubah ke dalam bentuk representasi numerik menggunakan metode TF-IDF. Representasi ini selanjutnya digunakan sebagai masukan pada proses pelatihan dan pengujian model analisis sentimen. Pada tahap ini, pengujian dilakukan untuk mengetahui kemampuan model Naive Bayes dan Support Vector Machine (SVM) dalam mengklasifikasikan ulasan ke dalam dua kategori sentimen, yaitu positif dan negatif.

Sebelum proses pelatihan model dilakukan, distribusi label hasil *preprocessing* terlebih dahulu dianalisis untuk mengetahui komposisi kelas pada dataset penelitian. Visualisasi distribusi data hasil *preprocessing* ditunjukkan pada Gambar 5.30.

Gambar 5.30 Distribusi Data Hasil Preprocessing

Berdasarkan Gambar 5.30, terlihat bahwa dataset didominasi oleh ulasan dengan sentimen positif, sedangkan jumlah ulasan negatif jauh lebih sedikit. Kondisi ini menunjukkan adanya ketidakseimbangan kelas (*class imbalance*) yang cukup signifikan. Dalam permasalahan klasifikasi teks, ketidakseimbangan kelas perlu diperhatikan karena dapat menyebabkan model lebih banyak mempelajari pola dari kelas mayoritas dibandingkan kelas minoritas. Akibatnya, model dapat menghasilkan nilai *accuracy* yang tinggi, tetapi belum tentu memiliki kemampuan yang baik dalam mengenali kelas minoritas, yaitu sentimen negatif.

Pada konteks penelitian ini, sentimen negatif justru memiliki nilai penting dalam proses monitoring karena dapat merepresentasikan keluhan, kritik, atau pengalaman tidak memuaskan dari pelanggan. Oleh karena itu, apabila model terlalu bias terhadap kelas positif, maka sistem berisiko kurang sensitif dalam mendeteksi ulasan yang memerlukan perhatian pengelola hotel. Atas dasar tersebut, penelitian ini tidak hanya melakukan pengujian pada distribusi data asli yang tidak seimbang, tetapi juga menerapkan penyeimbangan data latih menggunakan teknik *resampling* pada kelas minoritas.

Tujuan utama dari *resampling* adalah untuk memberikan komposisi data yang lebih seimbang pada tahap pelatihan, sehingga model memiliki kesempatan yang lebih baik untuk mempelajari pola sentimen negatif. Dengan cara ini, model diharapkan tidak terlalu condong pada kelas mayoritas dan dapat memberikan performa yang lebih adil terhadap kedua kelas. Perlu dicatat bahwa proses *resampling* hanya diterapkan pada data latih, sedangkan data uji tetap dipertahankan dalam distribusi aslinya agar evaluasi model tetap mencerminkan kondisi data nyata di lapangan.

Pembagian data pada tahap pemodelan dilakukan dengan proporsi 80:20 antara data latih dan data uji. Berdasarkan data eksperimen, jumlah data latih sebanyak 1.740 ulasan yang terdiri atas 1.592 ulasan positif dan 148 ulasan negatif. Sementara itu, data uji berjumlah 435 ulasan yang terdiri atas 398 ulasan positif dan 37 ulasan negatif. Visualisasi distribusi data latih dan data uji ditunjukkan pada Gambar 5.31.

Gambar 5.31 Distribusi Data Latih dan Data Uji

Berdasarkan Gambar 5.31, terlihat bahwa distribusi kelas pada data latih maupun data uji masih didominasi oleh ulasan positif. Selanjutnya, setelah dilakukan *resampling* pada data latih, distribusi kelas menjadi lebih seimbang sebagaimana ditunjukkan pada Gambar 5.32.

Gambar 5.32 Distribusi Data Latih Setelah *Resampling* dan Data Uji

Keberadaan dua visualisasi tersebut menunjukkan bahwa penelitian ini membandingkan dua kondisi, yaitu kondisi distribusi asli dan kondisi setelah penyeimbangan data latih. Dengan demikian, pengaruh *resampling* terhadap performa model dapat dianalisis secara lebih jelas, baik dari sisi prediksi keseluruhan maupun dari sisi kemampuan model dalam mengenali kelas minoritas.

Selain pembagian data dan penyeimbangan kelas, proses pembentukan fitur menghasilkan kosakata TF-IDF sebanyak 5.123 fitur. Representasi fitur tersebut menjadi dasar bagi model Naive Bayes dan Support Vector Machine dalam mempelajari pola sentimen dari teks ulasan Google Maps. Hasil evaluasi model pada skenario distribusi data asli yang tidak seimbang ditunjukkan pada Tabel 5.5, sedangkan hasil evaluasi pada skenario data latih yang telah diseimbangkan melalui *resampling* ditunjukkan pada Tabel 5.6.

Tabel 5.5 Hasil Evaluasi Model pada Skenario Distribusi Kelas Asli yang Tidak Seimbang

| Model | Accuracy | Precision Weighted | Recall Weighted | F1 Weighted | F1 Macro | Balanced Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| Naive Bayes | 0,9494 | 0,9451 | 0,9494 | 0,9449 | 0,8090 | 0,7640 |
| SVM | 0,9425 | 0,9534 | 0,9425 | 0,9463 | 0,8404 | 0,8950 |

Selanjutnya, hasil evaluasi model pada skenario data latih yang telah diseimbangkan melalui *resampling* kelas minoritas ditunjukkan pada Tabel 5.6.

Tabel 5.6 Hasil Evaluasi Model pada Skenario Penyeimbangan Data Latih dengan *Resampling* Kelas Minoritas

| Model | Accuracy | Precision Weighted | Recall Weighted | F1 Weighted | F1 Macro | Balanced Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| Naive Bayes | 0,9402 | 0,9450 | 0,9402 | 0,9422 | 0,8210 | 0,8448 |
| SVM | 0,9540 | 0,9514 | 0,9540 | 0,9522 | 0,8405 | 0,8155 |

Berdasarkan proses *tuning* yang dilakukan, diperoleh parameter terbaik untuk masing-masing model pada masing-masing skenario sebagai berikut.

1. Skenario tanpa penyeimbangan:
   Naive Bayes menggunakan `alpha = 1,0`, sedangkan SVM menggunakan `C = 0,05`.
2. Skenario dengan penyeimbangan data latih:
   Naive Bayes menggunakan `alpha = 0,01`, sedangkan SVM menggunakan `C = 2`.
3. Ukuran kosakata TF-IDF pada kedua skenario adalah `5123` fitur.

Berdasarkan hasil pengujian tersebut, model SVM pada skenario penyeimbangan data latih melalui *resampling* kelas minoritas menghasilkan nilai *accuracy* tertinggi, yaitu sebesar 0,9540. Hal ini menunjukkan bahwa pada kondisi data latih yang telah diseimbangkan, SVM memiliki kemampuan terbaik dalam menghasilkan prediksi benar secara keseluruhan. Namun, nilai *balanced accuracy* tertinggi justru diperoleh model SVM pada skenario distribusi kelas asli yang tidak seimbang, yaitu sebesar 0,8950. Hasil ini menunjukkan bahwa peningkatan performa model akibat *resampling* tidak selalu terjadi secara konsisten pada seluruh metrik evaluasi.

Jika ditinjau lebih rinci, model Naive Bayes tetap menunjukkan performa yang kompetitif pada kedua skenario. Penerapan penyeimbangan data latih pada Naive Bayes memang menurunkan *accuracy* dari 0,9494 menjadi 0,9402, tetapi meningkatkan nilai *F1 Macro* dari 0,8090 menjadi 0,8210 dan *balanced accuracy* dari 0,7640 menjadi 0,8448. Peningkatan ini menunjukkan bahwa *resampling* membantu Naive Bayes menjadi lebih baik dalam mengenali kelas minoritas, sehingga performa antar kelas menjadi lebih seimbang.

Di sisi lain, model SVM menunjukkan karakteristik yang berbeda. Pada skenario penyeimbangan data latih, SVM menghasilkan *accuracy* tertinggi sebesar 0,9540 dan *F1 Weighted* sebesar 0,9522. Akan tetapi, *balanced accuracy* SVM justru menurun dari 0,8950 pada skenario tanpa penyeimbangan menjadi 0,8155 pada skenario dengan penyeimbangan. Temuan ini menunjukkan bahwa *resampling* tidak selalu meningkatkan seluruh metrik evaluasi secara bersamaan, khususnya pada model yang sejak awal sudah cukup kuat dalam membedakan kelas.

Hasil tersebut menunjukkan bahwa *resampling* diperlukan bukan semata-mata untuk meningkatkan *accuracy*, tetapi untuk membantu model mempelajari kelas minoritas secara lebih proporsional. Dengan adanya *resampling*, evaluasi model menjadi lebih bermakna karena dapat menunjukkan apakah model benar-benar membaik dalam mengenali kedua kelas, bukan hanya semakin baik pada kelas mayoritas. Oleh karena itu, penggunaan *resampling* pada penelitian ini penting untuk memberikan gambaran yang lebih lengkap mengenai perilaku model ketika menghadapi data yang tidak seimbang.

Secara keseluruhan, SVM tetap menjadi model yang paling kuat untuk dipertimbangkan dalam integrasi ke sistem operasional karena mampu memberikan performa tinggi secara umum, terutama pada *accuracy*, *F1 Weighted*, dan *F1 Macro*. Namun demikian, hasil penelitian ini juga menegaskan bahwa evaluasi model klasifikasi tidak cukup hanya didasarkan pada satu metrik. Metrik seperti *F1 Macro* dan *balanced accuracy* tetap perlu diperhatikan agar kemampuan model dalam mengklasifikasikan setiap kelas sentimen dapat dinilai secara lebih menyeluruh dan seimbang.

Berdasarkan seluruh hasil evaluasi tersebut, model yang dipilih sebagai model terbaik dalam penelitian ini adalah Support Vector Machine pada skenario penyeimbangan data latih melalui *resampling* kelas minoritas. Pemilihan ini didasarkan pada capaian *accuracy* tertinggi sebesar 0,9540, didukung *F1 Weighted* sebesar 0,9522 dan *F1 Macro* sebesar 0,8405 yang menunjukkan performa klasifikasi yang kuat secara umum. Meskipun demikian, hasil SVM pada skenario tanpa penyeimbangan tetap menjadi temuan penting karena menghasilkan *balanced accuracy* tertinggi sebesar 0,8950. Dengan demikian, keputusan pemilihan model terbaik dalam penelitian ini mempertimbangkan performa agregat secara keseluruhan, sekaligus tetap mencatat bahwa kemampuan model dalam menjaga keseimbangan klasifikasi antar kelas juga merupakan aspek yang penting.

Selain hasil evaluasi akhir, proses eksperimen ini juga menunjukkan bahwa performa model dipengaruhi oleh seluruh tahapan pengolahan data, mulai dari pelabelan, *preprocessing*, pembentukan fitur TF-IDF, pembagian data latih dan data uji, hingga penyeimbangan data latih. Dengan demikian, performa model analisis sentimen pada penelitian ini tidak hanya ditentukan oleh pemilihan algoritma klasifikasi, tetapi juga oleh kualitas tahapan persiapan data yang dilakukan sebelumnya.

#### 5.2.5 Hasil Antarmuka

Hasil implementasi antarmuka menunjukkan bahwa sistem telah berhasil menerjemahkan proses monitoring sentimen ke dalam bentuk tampilan web yang informatif, terstruktur, dan mudah digunakan. Antarmuka yang dibangun tidak hanya berfungsi sebagai media interaksi pengguna, tetapi juga menjadi jembatan antara proses komputasi di sisi backend dengan kebutuhan operasional pengguna dalam memantau ulasan hotel. Melalui antarmuka ini, pengguna dapat melakukan autentikasi, melihat hasil analisis sentimen, memantau tren ulasan, mengelola subscriber Telegram, serta meninjau status pengiriman notifikasi secara terintegrasi.

Secara umum, hasil implementasi antarmuka memperlihatkan bahwa sistem telah mampu menyajikan data dari basis data dan hasil klasifikasi model ke dalam tampilan yang mudah dipahami. Hal ini penting karena nilai praktis dari sistem monitoring tidak hanya ditentukan oleh ketepatan model analisis sentimen, tetapi juga oleh kemampuan sistem dalam menyajikan informasi secara cepat, jelas, dan dapat ditindaklanjuti oleh pengguna. Oleh karena itu, subbab ini membahas hasil implementasi beberapa halaman utama pada sistem.

a. Halaman Login

Halaman login merupakan pintu masuk utama pengguna ke dalam sistem monitoring sentimen. Melalui halaman ini, pengguna memasukkan `username` dan `password` untuk memperoleh akses ke dashboard sesuai hak akses yang dimiliki. Dari sisi tampilan, halaman login dirancang sederhana, terpusat, dan mudah digunakan saat pertama kali mengakses aplikasi. Hasil implementasi halaman login ditunjukkan pada Gambar 5.31.
Gambar 5.31 Hasil Halaman Login

Pada hasil implementasinya, halaman login tidak hanya berfungsi sebagai antarmuka autentikasi, tetapi juga mendukung pengelolaan akses yang aman melalui proses verifikasi akun di sisi backend. Dengan demikian, halaman ini menjadi komponen awal yang memastikan bahwa hanya pengguna terdaftar yang dapat mengakses fitur monitoring.

b. Halaman Register

Halaman register digunakan untuk melakukan pendaftaran akun baru sekaligus pembuatan data hotel yang akan dipantau pada sistem. Melalui halaman ini, pengguna dapat mengisi informasi dasar akun dan informasi hotel sebelum sistem menyimpan data tersebut ke basis data. Hasil implementasi halaman register ditunjukkan pada Gambar 5.32.

Gambar 5.32 Hasil Halaman Register

Hasil implementasi halaman register menunjukkan bahwa sistem telah mendukung proses *onboarding* pengguna baru secara terintegrasi. Keberadaan halaman ini penting karena proses registrasi tidak hanya menambahkan akun pengguna, tetapi juga langsung menghubungkannya dengan hotel yang akan menjadi objek monitoring pada sistem.

c. Halaman Dashboard

Halaman dashboard merupakan pusat monitoring pada sistem yang menampilkan ringkasan informasi utama, seperti hotel aktif, jumlah ulasan, distribusi sentimen, rating rata-rata, ulasan terbaru, dan kontrol scheduler otomatis. Halaman ini menjadi tampilan utama setelah pengguna berhasil melakukan login. Hasil implementasi halaman dashboard ditunjukkan pada Gambar 5.33.

Gambar 5.33 Hasil Halaman Dashboard

Melalui dashboard, pengguna dapat memperoleh gambaran kondisi sentimen hotel secara cepat dalam satu tampilan. Hasil implementasi halaman ini menunjukkan bahwa data hasil scraping, hasil klasifikasi sentimen, dan data dari basis data berhasil diintegrasikan ke dalam bentuk visual yang informatif dan mudah dipahami. Dengan demikian, dashboard berfungsi sebagai pusat informasi utama bagi pengguna dalam melakukan monitoring operasional.

d. Halaman Analitik

Halaman analitik digunakan untuk menyajikan visualisasi distribusi sentimen dan tren ulasan harian secara lebih rinci. Melalui halaman ini, pengguna dapat melihat dinamika perubahan sentimen dalam bentuk grafik yang mendukung proses evaluasi layanan. Hasil implementasi halaman analitik ditunjukkan pada Gambar 5.34.

Gambar 5.34 Hasil Halaman Analitik

Hasil implementasi halaman analitik menunjukkan bahwa sistem mampu menyajikan data statistik dan tren sentimen secara visual dan dinamis. Keberadaan halaman ini membuat informasi hasil analisis tidak hanya ditampilkan dalam bentuk tabel, tetapi juga dalam bentuk grafik yang lebih mudah dibaca untuk kebutuhan pemantauan dan pengambilan keputusan.

e. Halaman Subscriber

Halaman subscriber digunakan untuk mengelola daftar pengguna Telegram yang menerima notifikasi dari sistem. Pada halaman ini, pengguna dapat menambahkan `chat_id`, menghapus subscriber, serta mengontrol bot Telegram melalui antarmuka web. Hasil implementasi halaman subscriber ditunjukkan pada Gambar 5.35.

Gambar 5.35 Hasil Halaman Subscriber
   
Hasil implementasi halaman subscriber menunjukkan bahwa sistem tidak hanya mampu melakukan analisis sentimen, tetapi juga mendukung distribusi informasi kepada pihak yang berkepentingan. Halaman ini memperlihatkan integrasi antara aplikasi web, basis data, dan Telegram Bot API dalam proses pengelolaan subscriber.

f. Halaman Notifikasi

Halaman notifikasi berfungsi untuk menampilkan riwayat pengiriman notifikasi otomatis kepada subscriber melalui Telegram Bot. Informasi yang ditampilkan meliputi identitas ulasan, `chat_id`, status pengiriman, serta waktu pengiriman notifikasi. Hasil implementasi halaman notifikasi ditunjukkan pada Gambar 5.36.

Gambar 5.36 Hasil Halaman Notifikasi

Hasil implementasi halaman notifikasi menunjukkan bahwa sistem telah menyediakan mekanisme audit terhadap distribusi informasi. Melalui halaman ini, pengguna atau administrator dapat memantau apakah hasil monitoring berhasil dikirimkan kepada subscriber yang terdaftar, sehingga proses notifikasi menjadi lebih transparan dan dapat ditelusuri.

g. Halaman Riwayat Ulasan

Halaman riwayat ulasan digunakan untuk menampilkan riwayat ulasan pelanggan yang telah diproses oleh sistem klasifikasi sentimen. Halaman ini menampilkan data ulasan, rating, waktu ulasan, serta hasil prediksi Naive Bayes dan Support Vector Machine dalam bentuk tabel. Hasil implementasi halaman riwayat ulasan ditunjukkan pada Gambar 5.37.

Gambar 5.37 Hasil Halaman Riwayat Ulasan

Hasil implementasi halaman riwayat ulasan menunjukkan bahwa sistem telah menyediakan transparansi terhadap data ulasan dan hasil klasifikasi. Melalui halaman ini, pengguna dapat menelusuri kembali data yang telah diproses dan membandingkan hasil prediksi kedua model secara langsung. Halaman ini juga memperkuat fungsi sistem sebagai alat monitoring yang tidak hanya menampilkan ringkasan, tetapi juga menyediakan detail data yang telah dianalisis.

Secara keseluruhan, implementasi antarmuka menunjukkan bahwa sistem telah berhasil mengintegrasikan komponen frontend, backend, basis data, dan layanan eksternal ke dalam satu pengalaman penggunaan yang utuh. Dengan demikian, hasil analisis sentimen tidak hanya diproses secara komputasional, tetapi juga dapat dimanfaatkan secara langsung oleh pengguna untuk kebutuhan monitoring operasional dan evaluasi layanan hotel.

#### 5.2.6 Hasil Pengujian Fungsional Sistem

Berdasarkan pengujian fungsional terhadap aplikasi, sistem telah berhasil mengimplementasikan fungsi-fungsi utama sebagaimana ditunjukkan pada Tabel 5.7. Pengujian dilakukan dengan menguji setiap fitur utama sistem berdasarkan langkah penggunaan, keluaran yang diharapkan, keluaran aktual sistem, dan status keberhasilannya.

Tabel 5.7 Hasil Pengujian Fungsional Sistem

| No | Fitur yang Diuji | Langkah Uji | Output yang Diharapkan | Output Aktual Sistem | Status |
|---|---|---|---|---|---|
| 1 | Register pengguna | Pengguna mengisi formulir register dan mengirim data akun serta hotel | Sistem menyimpan akun baru dan data hotel, kemudian mengarahkan pengguna ke halaman login | Sistem berhasil membuat akun dan hotel baru melalui proses register, lalu mengarahkan pengguna ke halaman login | Berhasil |
| 2 | Login pengguna | Pengguna memasukkan username dan password yang valid | Sistem memverifikasi akun, menyimpan sesi login, dan mengarahkan pengguna ke halaman yang sesuai | Sistem memverifikasi kredensial, menyimpan sesi pengguna, dan mengarahkan ke dashboard pengguna atau admin sesuai peran | Berhasil |
| 3 | Isolasi data berdasarkan hotel aktif | Pengguna login menggunakan akun yang terhubung ke hotel tertentu | Sistem hanya menampilkan data sesuai hotel aktif pengguna | Sistem hanya memuat data ulasan, sentimen, dan notifikasi sesuai `active_hotel_id` pengguna | Berhasil |
| 4 | Scraping ulasan terbaru melalui SerpAPI | Sistem menjalankan proses scraping manual atau melalui scheduler | Sistem mengambil ulasan terbaru dari Google Maps berdasarkan `place_id` hotel | Sistem berhasil mengambil ulasan terbaru melalui SerpAPI dan mengubahnya ke format data operasional | Berhasil |
| 5 | Deteksi duplikasi ulasan | Sistem menerima ulasan yang sudah pernah tersimpan | Sistem menolak penyimpanan data duplikat | Sistem berhasil melakukan pengecekan duplikasi berdasarkan hotel, pengguna, teks ulasan, rating, dan sumber data | Berhasil |
| 6 | Prediksi sentimen menggunakan Naive Bayes dan SVM | Sistem memproses ulasan baru yang berhasil diambil | Sistem menghasilkan label sentimen dari kedua model | Sistem berhasil menghasilkan prediksi sentimen POSITIF atau NEGATIF menggunakan model Naive Bayes dan SVM | Berhasil |
| 7 | Penyimpanan hasil ke basis data | Sistem selesai memproses ulasan dan prediksi sentimen | Data ulasan dan hasil klasifikasi tersimpan ke basis data | Sistem berhasil menyimpan data ulasan, hasil sentimen, subscriber, dan log notifikasi ke basis data MySQL/MariaDB | Berhasil |
| 8 | Penampilan hasil pada dashboard dan riwayat ulasan | Pengguna membuka halaman dashboard dan riwayat ulasan | Sistem menampilkan ringkasan sentimen, ulasan terbaru, dan riwayat klasifikasi | Sistem berhasil menampilkan data hotel aktif, statistik sentimen, ulasan terbaru, dan tabel riwayat ulasan secara dinamis | Berhasil |
| 9 | Penjadwalan scraping otomatis melalui scheduler | Pengguna menjalankan scheduler dari antarmuka web | Sistem menjalankan scraping dan pipeline monitoring sesuai interval yang ditentukan | Sistem berhasil menjalankan scheduler berbasis interval dan memperbarui data secara berkala | Berhasil |
| 10 | Pendaftaran subscriber melalui Telegram Bot | Pengguna mengirim perintah `/start <hotel_id>` ke bot Telegram | Sistem menyimpan `chat_id` pengguna dan mengaitkannya dengan hotel yang dipilih | Sistem berhasil menyimpan `chat_id` subscriber ke basis data sesuai `hotel_id` yang diberikan | Berhasil |
| 11 | Pengiriman notifikasi ke subscriber Telegram | Sistem mendeteksi ulasan baru dan subscriber aktif tersedia | Sistem mengirimkan pesan notifikasi otomatis ke subscriber Telegram | Sistem berhasil mengirimkan pesan notifikasi yang memuat data ulasan dan hasil prediksi sentimen ke subscriber yang terdaftar | Berhasil |
| 12 | Pencatatan log notifikasi | Sistem selesai mengirimkan notifikasi Telegram | Sistem menyimpan riwayat pengiriman notifikasi | Sistem berhasil mencatat `review_id`, `chat_id`, status pengiriman, dan waktu pengiriman pada tabel notifikasi | Berhasil |

Hasil tersebut menunjukkan bahwa seluruh komponen utama sistem telah berjalan sesuai fungsi yang dirancang pada tahap analisis dan perancangan.

Secara fungsional, pengujian ini memperlihatkan bahwa alur utama sistem telah berjalan secara utuh, mulai dari autentikasi pengguna, penentuan hotel aktif, pengambilan ulasan terbaru, proses klasifikasi sentimen, penyimpanan ke basis data, hingga distribusi notifikasi melalui Telegram. Dengan demikian, hasil pengujian tidak hanya menunjukkan keberhasilan pada level fitur terpisah, tetapi juga pada integrasi antarkomponen dalam satu alur monitoring yang berkelanjutan.

Meskipun seluruh fitur utama telah berfungsi sesuai kebutuhan, masih terdapat beberapa aspek yang dapat dikembangkan lebih lanjut, seperti perluasan cakupan data ulasan, peningkatan kualitas pelabelan data, evaluasi beban sistem pada skala penggunaan yang lebih besar, serta pengembangan mekanisme pembaruan data yang lebih mendekati real-time. Dengan demikian, sistem yang dibangun telah layak digunakan sebagai prototipe operasional, namun masih terbuka untuk penyempurnaan pada penelitian dan pengembangan selanjutnya.

### 5.3 Pembahasan

#### 5.3.1 Pembahasan Hasil Model Analisis

Hasil evaluasi menunjukkan bahwa tidak ada satu model yang unggul mutlak pada seluruh metrik. Pada skenario distribusi kelas asli yang tidak seimbang, Naive Bayes memperoleh *accuracy* yang tinggi, yaitu 0,9494. Namun, SVM menunjukkan keunggulan pada metrik yang lebih sensitif terhadap distribusi kelas, khususnya *F1 Macro* sebesar 0,8404 dan *balanced accuracy* sebesar 0,8950. Hal ini menunjukkan bahwa SVM lebih mampu mempertahankan keseimbangan performa antar kelas pada data yang tidak seimbang.

Pada skenario penyeimbangan data latih melalui *resampling* kelas minoritas, dampak yang muncul berbeda pada masing-masing model. Naive Bayes mengalami penurunan *accuracy* dari 0,9494 menjadi 0,9402, tetapi nilai *F1 Macro* meningkat dari 0,8090 menjadi 0,8210 dan *balanced accuracy* meningkat dari 0,7640 menjadi 0,8448. Temuan ini menunjukkan bahwa penyeimbangan data latih membantu Naive Bayes menjadi lebih baik dalam mengenali kelas minoritas meskipun ketepatan prediksi keseluruhan sedikit menurun.

Sementara itu, SVM pada skenario penyeimbangan data latih menghasilkan *accuracy* tertinggi sebesar 0,9540 dengan *F1 Weighted* sebesar 0,9522 dan *F1 Macro* sebesar 0,8405. Meskipun demikian, nilai *balanced accuracy* justru menurun menjadi 0,8155 dibandingkan skenario tanpa penyeimbangan. Dengan demikian, penyeimbangan data latih memang meningkatkan performa keseluruhan SVM pada metrik agregat tertentu, tetapi tidak selalu meningkatkan kemampuannya secara merata pada seluruh kelas.

Dengan demikian, pemilihan model terbaik tidak seharusnya hanya didasarkan pada satu metrik. Jika fokus penelitian diarahkan pada proporsi prediksi benar secara keseluruhan, maka SVM pada skenario penyeimbangan data latih melalui *resampling* kelas minoritas merupakan pilihan yang paling kuat. Namun, apabila penekanan diarahkan pada keseimbangan performa antar kelas, maka hasil SVM pada skenario distribusi kelas asli yang tidak seimbang serta peningkatan performa Naive Bayes setelah penyeimbangan data juga menjadi temuan yang penting untuk dipertimbangkan.

Dari sudut pandang implementasi, temuan ini juga relevan karena sistem monitoring tidak hanya membutuhkan model yang akurat secara umum, tetapi juga model yang cukup sensitif dalam membaca ulasan dengan distribusi kelas yang tidak selalu seimbang. Dalam konteks operasional hotel, kegagalan mendeteksi ulasan negatif dapat berdampak lebih besar dibanding kesalahan klasifikasi pada ulasan positif. Oleh sebab itu, penggunaan beberapa metrik evaluasi dalam penelitian ini menjadi penting untuk memastikan model yang dipilih benar-benar sesuai dengan kebutuhan sistem monitoring.

#### 5.3.2 Pembahasan Implementasi Sistem Monitoring

Dari sisi implementasi aplikasi, hasil penelitian menunjukkan bahwa sistem monitoring yang dibangun telah berhasil menjalankan alur operasional secara utuh, mulai dari pengambilan data ulasan, klasifikasi sentimen, penyimpanan hasil, penyajian visualisasi, hingga pengiriman notifikasi otomatis. Temuan ini penting karena menunjukkan bahwa penelitian tidak berhenti pada tahap eksperimen model, tetapi telah diwujudkan ke dalam aplikasi yang dapat digunakan secara langsung untuk kebutuhan monitoring ulasan hotel.

Hasil pengujian fungsional memperlihatkan bahwa modul scraping mampu mengambil ulasan terbaru berdasarkan hotel aktif, kemudian meneruskannya ke proses klasifikasi sentimen menggunakan model Naive Bayes dan SVM. Setelah proses klasifikasi selesai, data ulasan beserta hasil prediksi berhasil disimpan ke basis data dan ditampilkan kembali pada antarmuka sistem. Hal ini menunjukkan bahwa integrasi antara komponen akuisisi data, inferensi model, dan penyimpanan data telah berjalan dengan baik dalam satu alur kerja yang konsisten.

Dari sudut pandang penggunaan, hasil implementasi dashboard menunjukkan bahwa sistem telah mampu menyajikan ringkasan kondisi hotel secara cepat melalui informasi jumlah ulasan, distribusi sentimen, rating rata-rata, dan ulasan terbaru. Halaman analitik memperkuat fungsi tersebut dengan menyajikan tren sentimen dan distribusi ulasan secara visual, sehingga pengguna tidak hanya menerima data mentah, tetapi juga dapat memahami pola perubahan opini pelanggan dari waktu ke waktu. Dengan demikian, aplikasi monitoring yang dibangun tidak hanya berfungsi sebagai tempat penyimpanan hasil analisis, tetapi juga sebagai media interpretasi informasi yang mendukung pengambilan keputusan.

Halaman riwayat ulasan dan notifikasi juga memberikan kontribusi penting terhadap hasil implementasi sistem. Halaman riwayat ulasan memungkinkan pengguna menelusuri kembali data ulasan yang telah diproses beserta hasil prediksi kedua model, sehingga proses monitoring memiliki jejak data yang transparan dan dapat diverifikasi. Di sisi lain, halaman notifikasi dan subscriber menunjukkan bahwa sistem telah berhasil memperluas fungsi monitoring dari sekadar visualisasi di web menjadi distribusi informasi secara aktif melalui Telegram Bot. Implikasi praktisnya adalah pengguna tidak harus selalu membuka aplikasi untuk mengetahui adanya ulasan baru, karena sistem dapat mengirimkan informasi tersebut secara otomatis.

Keberhasilan implementasi scheduler juga menjadi bagian penting dari hasil aplikasi monitoring secara keseluruhan. Dengan adanya scheduler, proses scraping dan monitoring dapat dijalankan secara berkala tanpa intervensi manual. Kondisi ini membuat sistem lebih dekat dengan kebutuhan operasional nyata, karena pengguna tidak lagi bergantung pada pemeriksaan manual yang cenderung lambat dan tidak konsisten. Dalam konteks ini, implementasi sistem lebih tepat disebut bersifat *near real-time*, karena pembaruan data dilakukan secara berkala dan sudah cukup mendukung pemantauan ulasan secara berkelanjutan.

Aspek lain yang penting dari hasil implementasi adalah penerapan isolasi data berdasarkan hotel aktif dan pengelolaan akses berbasis peran. Mekanisme ini memastikan bahwa setiap pengguna hanya dapat mengakses data yang sesuai dengan lingkup hotelnya, sehingga keamanan dan konsistensi data lebih terjaga. Selain itu, area administrasi memungkinkan pengelolaan hotel, pengguna, ulasan, dan hasil sentimen secara lebih terstruktur. Temuan ini menunjukkan bahwa aplikasi yang dibangun tidak hanya berfungsi pada level analisis data, tetapi juga telah memperhatikan kebutuhan tata kelola informasi dalam lingkungan sistem yang sesungguhnya.

Secara keseluruhan, pembahasan implementasi sistem monitoring menunjukkan bahwa hasil aplikasi tidak hanya berhasil dari sisi teknis pengembangan perangkat lunak, tetapi juga memberikan nilai praktis dalam konteks operasional hotel. Sistem mampu menghubungkan proses akuisisi data, analisis sentimen, visualisasi, penyimpanan, dan notifikasi ke dalam satu platform yang saling terintegrasi. Dengan demikian, aplikasi yang dibangun telah memenuhi tujuan penelitian sebagai sistem monitoring ulasan hotel berbasis web yang dapat membantu pengguna memantau sentimen pelanggan secara lebih cepat, terstruktur, dan terdokumentasi.

#### 5.3.3 Keterbatasan Penelitian

Meskipun sistem telah berhasil diimplementasikan, terdapat beberapa keterbatasan yang perlu dijelaskan secara akademik.

1. Data penelitian masih terbatas pada domain hotel tertentu, sehingga generalisasi model ke domain lain belum dapat dipastikan.
2. Pelabelan data latih dilakukan menggunakan *weak supervision* berbasis model transformer pra-latih, bukan anotasi manual penuh.
3. Keandalan sistem operasional dipengaruhi oleh layanan eksternal, terutama SerpAPI dan Telegram Bot API.
4. Sistem bersifat *near real-time* berbasis scheduler, sehingga kecepatan deteksi ulasan baru bergantung pada interval scraping.
5. Evaluasi pada penelitian ini lebih banyak menekankan metrik klasifikasi, sedangkan evaluasi beban sistem dan pengalaman pengguna belum dibahas secara mendalam.

Keterbatasan tersebut menunjukkan bahwa hasil penelitian ini perlu dipahami sesuai ruang lingkup yang telah ditetapkan. Dengan demikian, sistem yang dibangun dapat dinilai berhasil pada konteks penelitian ini, tetapi masih terbuka untuk pengembangan lanjutan pada aspek data, metode pelabelan, ketahanan sistem, dan evaluasi implementasi secara lebih luas. Penyampaian keterbatasan ini juga penting agar laporan tetap jujur secara ilmiah dan tidak menimbulkan klaim yang berlebihan.

#### 5.3.4 Implikasi Hasil Penelitian

Secara praktis, sistem yang dibangun dapat membantu pengelola hotel memantau opini pelanggan secara lebih cepat, terstruktur, dan terdokumentasi. Ulasan baru yang masuk tidak perlu lagi diperiksa satu per satu secara manual melalui Google Maps, karena sistem telah menyediakan mekanisme akuisisi, analisis, visualisasi, dan notifikasi secara terintegrasi. Implikasi ini penting bagi operasional hotel karena ulasan pelanggan dapat langsung diidentifikasi, dikategorikan, dan ditindaklanjuti berdasarkan kecenderungan sentimennya.

Dari sisi pengambilan keputusan, keberadaan dashboard, halaman analitik, riwayat ulasan, notifikasi, dan subscriber menunjukkan bahwa hasil analisis sentimen dapat diubah menjadi informasi yang lebih mudah dimanfaatkan oleh pengguna nonteknis. Hal ini berarti sistem tidak hanya memberikan keluaran prediksi, tetapi juga mendukung proses monitoring layanan secara berkelanjutan, terutama dalam mendeteksi ulasan negatif yang memerlukan respons lebih cepat.

Secara akademik, penelitian ini menunjukkan bahwa kombinasi TF-IDF dengan model machine learning klasik seperti Naive Bayes dan SVM masih relevan untuk analisis sentimen teks berbahasa Indonesia, khususnya pada domain ulasan hotel. Hasil eksperimen juga menegaskan pentingnya evaluasi multi-metrik dalam penentuan model terbaik, terutama pada kondisi data yang tidak seimbang. Temuan ini memperlihatkan bahwa penilaian performa model tidak cukup hanya berdasarkan *accuracy*, tetapi perlu mempertimbangkan *F1 Macro* dan *balanced accuracy* agar interpretasi hasil menjadi lebih komprehensif.

Dengan demikian, implikasi hasil penelitian ini tidak hanya terletak pada keberhasilan membangun aplikasi monitoring sentimen, tetapi juga pada kontribusinya dalam menunjukkan hubungan antara kualitas persiapan data, strategi penyeimbangan kelas, pemilihan model, dan kegunaan sistem dalam konteks operasional nyata.
