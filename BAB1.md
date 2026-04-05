## BAB I PENDAHULUAN

### 1.1 Latar Belakang

Industri perhotelan merupakan salah satu sektor jasa yang sangat bergantung pada persepsi dan tingkat kepuasan pelanggan. Reputasi hotel tidak hanya dibentuk oleh kualitas fasilitas dan layanan yang diberikan, tetapi juga oleh bagaimana pengalaman pelanggan tersebut disampaikan kepada publik. Dalam konteks digital saat ini, pengalaman pelanggan semakin banyak dituangkan melalui platform ulasan daring (*online reviews*), sehingga ulasan pelanggan menjadi sumber informasi yang penting bagi calon tamu maupun pihak manajemen hotel.

Salah satu platform yang paling dominan dalam penyampaian ulasan pelanggan adalah Google Maps melalui fitur ulasan. Melalui platform ini, pelanggan dapat memberikan rating dan komentar tekstual yang mencerminkan kepuasan, keluhan, atau pengalaman mereka selama menggunakan layanan hotel. Ulasan dalam bentuk teks tersebut memiliki nilai strategis karena dapat memengaruhi reputasi daring hotel. Ulasan positif cenderung meningkatkan kepercayaan calon tamu, sedangkan ulasan negatif berpotensi menurunkan citra hotel dan memengaruhi keputusan konsumen dalam memilih tempat menginap.

Permasalahan muncul ketika jumlah ulasan pelanggan terus bertambah, tetapi tidak diimbangi dengan mekanisme pemantauan yang sistematis dan otomatis. Pada praktiknya, banyak pengelola hotel masih mengandalkan pemantauan manual dengan membaca ulasan satu per satu pada Google Maps. Cara ini menjadi tidak efisien ketika volume ulasan meningkat, karena pihak manajemen harus meluangkan waktu khusus untuk memeriksa setiap ulasan yang masuk. Kondisi tersebut meningkatkan risiko keterlambatan dalam mengenali ulasan yang bernada negatif dan membutuhkan tindak lanjut lebih cepat.

Kondisi serupa terjadi pada Aveta Hotel Malioboro. Berdasarkan pengamatan pada saat penelitian dilakukan, hotel ini memiliki jumlah ulasan pelanggan yang cukup besar di Google Maps. Banyaknya ulasan tersebut menunjukkan tingginya interaksi pelanggan, tetapi pada saat yang sama juga menambah beban pemantauan apabila proses evaluasi masih dilakukan secara manual. Tanpa dukungan sistem yang terstruktur, manajemen berisiko terlambat mendeteksi keluhan pelanggan, terutama pada periode operasional yang padat seperti akhir pekan atau jam sibuk.

Permasalahan menjadi semakin kompleks karena mekanisme notifikasi bawaan pada platform Google Maps belum tentu mendukung distribusi informasi secara optimal kepada seluruh pihak manajemen yang membutuhkan. Dalam banyak kasus, informasi ulasan baru hanya terhubung ke akun tertentu, sehingga tidak semua pihak yang bertanggung jawab dapat menerima informasi secara cepat dan serentak. Akibatnya, proses pemantauan sangat bergantung pada aktivitas pengecekan manual dan konsistensi masing-masing pengelola.

Untuk mengatasi permasalahan tersebut, diperlukan pendekatan yang mampu mengolah ulasan pelanggan secara otomatis, konsisten, dan cepat. Salah satu pendekatan yang relevan adalah analisis sentimen, yaitu teknik pengolahan teks yang digunakan untuk mengidentifikasi kecenderungan opini dalam suatu teks, misalnya ke dalam kategori positif dan negatif. Dengan analisis sentimen, ulasan pelanggan tidak hanya dibaca sebagai teks biasa, tetapi juga dapat dipetakan ke dalam informasi yang lebih terstruktur dan siap digunakan untuk mendukung pengambilan keputusan.

Pada penelitian ini, analisis sentimen diterapkan pada ulasan pelanggan Aveta Hotel Malioboro di Google Maps dengan menggunakan dua algoritma machine learning, yaitu Naive Bayes dan Support Vector Machine (SVM). Kedua algoritma tersebut dipilih karena memiliki karakteristik yang sesuai untuk klasifikasi teks. Naive Bayes dikenal sederhana, efisien, dan banyak digunakan sebagai pendekatan dasar dalam klasifikasi dokumen. Sementara itu, SVM dikenal efektif dalam menangani data berdimensi tinggi seperti representasi teks berbasis TF-IDF.

Namun demikian, sebagian besar penelitian terdahulu masih berhenti pada tahap evaluasi model klasifikasi sentimen secara statis. Hasil penelitian umumnya hanya menunjukkan performa algoritma pada dataset tertentu tanpa mengintegrasikan model tersebut ke dalam sistem monitoring yang dapat digunakan secara langsung. Padahal, dalam konteks kebutuhan operasional hotel, yang dibutuhkan bukan hanya model klasifikasi yang baik, tetapi juga sistem yang mampu mengambil ulasan terbaru, melakukan klasifikasi sentimen secara otomatis, menyimpan hasil, menampilkan informasi analitik, dan mengirimkan notifikasi kepada pihak terkait.

Berdasarkan kondisi tersebut, penelitian ini berfokus pada perancangan dan implementasi sistem monitoring ulasan hotel berbasis web yang terintegrasi dengan analisis sentimen dan notifikasi Telegram. Sistem yang dibangun memanfaatkan dataset historis Google Maps untuk membangun model klasifikasi sentimen, kemudian menggunakan SerpAPI untuk mengambil ulasan terbaru secara periodik pada sistem operasional. Dengan pendekatan tersebut, sistem diharapkan mampu membantu manajemen hotel dalam memantau ulasan pelanggan secara lebih cepat, terstruktur, dan berbasis data. Dalam konteks implementasi, karakter layanan sistem ini lebih tepat disebut **near real-time**, karena proses pembaruan data dilakukan secara berkala menggunakan scheduler, bukan melalui aliran data kontinu setiap saat.

### 1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam penelitian ini adalah sebagai berikut:

1. Bagaimana performa algoritma Naive Bayes dan Support Vector Machine (SVM) dalam mengklasifikasikan sentimen ulasan pelanggan hotel?
2. Bagaimana merancang dan mengimplementasikan sistem monitoring ulasan hotel berbasis web yang terintegrasi dengan analisis sentimen?
3. Bagaimana sistem menyajikan informasi hasil analisis dan notifikasi agar dapat mendukung kebutuhan manajemen hotel dalam memantau ulasan baru?

### 1.3 Batasan Masalah

Agar penelitian tidak menyimpang dari pokok pembahasan, maka batasan masalah yang digunakan adalah sebagai berikut:

1. Objek penelitian dibatasi pada ulasan pelanggan Aveta Hotel Malioboro yang diperoleh dari Google Maps.
2. Analisis sentimen dalam penelitian ini hanya mengklasifikasikan ulasan ke dalam dua kategori, yaitu sentimen positif dan sentimen negatif.
3. Data historis digunakan untuk proses pelatihan dan evaluasi model, sedangkan data ulasan terbaru digunakan untuk proses monitoring sistem.
4. Metode klasifikasi yang digunakan dalam penelitian ini dibatasi pada Naive Bayes dan Support Vector Machine (SVM).
5. Representasi fitur teks dilakukan menggunakan metode TF-IDF.
6. Sistem yang dibangun difokuskan pada monitoring sentimen ulasan dan pengiriman notifikasi otomatis melalui Telegram Bot.
7. Proses pengambilan, analisis, dan monitoring ulasan dilakukan secara otomatis pada interval waktu tertentu menggunakan scheduler. Oleh karena itu, sistem yang dibangun tidak memproses setiap ulasan baru secara langsung pada saat ulasan dipublikasikan, melainkan setelah siklus pembaruan berikutnya. Dengan karakteristik tersebut, layanan sistem pada penelitian ini termasuk soft real-time dan diimplementasikan dalam bentuk near real-time, sehingga tidak mencakup mekanisme pemrosesan data real-time penuh berbasis streaming.
8. Penelitian ini difokuskan pada klasifikasi sentimen ulasan secara umum ke dalam dua kategori menggunakan algoritma Naive Bayes dan Support Vector Machine (SVM), sehingga tidak mencakup analisis sentimen berdasarkan banyak kelas, aspek tertentu, maupun metode klasifikasi lainnya.

### 1.4 Tujuan Penelitian

Tujuan penelitian ini adalah sebagai berikut:

1. Membandingkan performa algoritma Naive Bayes dan Support Vector Machine (SVM) dalam klasifikasi sentimen ulasan pelanggan hotel.
2. Membangun model analisis sentimen berbasis TF-IDF dan machine learning untuk mengklasifikasikan ulasan ke dalam kategori POSITIF dan NEGATIF.
3. Merancang dan mengimplementasikan sistem monitoring ulasan hotel berbasis web yang terintegrasi dengan model analisis sentimen.
4. Mengintegrasikan sistem dengan Telegram Bot sebagai media notifikasi otomatis terhadap ulasan baru.

### 1.5 Manfaat Penelitian

Manfaat yang diharapkan dari penelitian ini adalah sebagai berikut:

1. Bagi penulis, penelitian ini memberikan pengalaman dan kontribusi dalam pengembangan sistem analisis sentimen berbasis machine learning serta integrasinya ke dalam aplikasi monitoring.
2. Bagi pihak hotel, penelitian ini menghasilkan sistem monitoring ulasan pelanggan yang dapat membantu manajemen memantau ulasan baru secara lebih cepat dan terstruktur.
3. Bagi pengguna sistem, integrasi dengan Telegram Bot memungkinkan distribusi informasi ulasan baru kepada beberapa pihak secara bersamaan tanpa bergantung pada satu akun Google Maps.
4. Bagi peneliti selanjutnya, penelitian ini dapat menjadi referensi dalam pengembangan sistem monitoring sentimen pada sektor jasa atau domain lain yang memiliki karakteristik serupa.

### 1.6 Sistematika Penulisan

Sistematika penulisan laporan tugas akhir ini disusun untuk memberikan gambaran yang terstruktur mengenai alur penelitian yang dilakukan. Laporan ini terdiri atas enam bab dengan uraian sebagai berikut:

1. **Bab I Pendahuluan**  
   Bab ini menguraikan latar belakang penelitian, rumusan masalah, batasan masalah, tujuan penelitian, manfaat penelitian, dan sistematika penulisan.

2. **Bab II Tinjauan Pustaka**  
   Bab ini membahas landasan teori dan penelitian terdahulu yang berkaitan dengan monitoring ulasan, analisis sentimen, text preprocessing, TF-IDF, Naive Bayes, Support Vector Machine, serta konsep lain yang relevan dengan penelitian.

3. **Bab III Metode Penelitian**  
   Bab ini menjelaskan metode penelitian yang digunakan, meliputi sumber data, prosedur pengumpulan data, aturan bisnis, tahapan penelitian, pelabelan data, preprocessing, ekstraksi fitur, pelatihan model, evaluasi model, implementasi sistem, dan pengujian sistem.

4. **Bab IV Analisis dan Perancangan Sistem**  
   Bab ini menguraikan analisis sistem yang berjalan, analisis sistem yang diusulkan, kebutuhan fungsional dan nonfungsional, perancangan logis, perancangan fisik basis data, serta arsitektur aplikasi yang menjadi dasar implementasi sistem.

5. **Bab V Implementasi, Hasil, dan Pembahasan**  
   Bab ini menyajikan implementasi teknis sistem, hasil pengujian model analisis sentimen, hasil implementasi aplikasi, serta pembahasan terhadap temuan penelitian dan keterbatasan sistem yang dibangun.

6. **Bab VI Penutup**  
   Bab ini berisi simpulan yang diperoleh dari hasil penelitian dan pembahasan, serta saran untuk pengembangan sistem dan penelitian lanjutan.
