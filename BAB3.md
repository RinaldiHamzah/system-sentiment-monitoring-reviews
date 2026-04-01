## BAB III METODE PENELITIAN

### 3.1 Metode Penelitian

Penelitian ini menggunakan metode rancang bangun sistem (*design and implementation*) yang dipadukan dengan eksperimen machine learning untuk analisis sentimen teks. Pendekatan ini dipilih karena tujuan penelitian tidak hanya terbatas pada evaluasi model klasifikasi, tetapi juga mencakup pembangunan sistem monitoring ulasan hotel yang dapat dioperasikan secara nyata.

Secara umum, penelitian dilaksanakan melalui beberapa tahapan utama, yaitu pengumpulan data, pelabelan data, preprocessing teks, ekstraksi fitur, pelatihan dan evaluasi model, integrasi model ke sistem, serta pengujian sistem monitoring secara menyeluruh. Dengan pendekatan tersebut, penelitian ini menghasilkan dua keluaran utama, yaitu model analisis sentimen dan aplikasi monitoring ulasan hotel berbasis web.

### 3.2 Bahan dan Sumber Data

#### 3.2.1 Data yang Digunakan

Data yang digunakan dalam penelitian ini berupa ulasan pelanggan Aveta Hotel Malioboro yang diperoleh dari platform Google Maps melalui fitur ulasan. Ulasan tersebut berbentuk data teks tidak terstruktur yang merepresentasikan opini pelanggan terhadap layanan, fasilitas, dan pengalaman menginap di hotel.

Secara umum, data ulasan memuat beberapa atribut, yaitu nama pengguna, tanggal ulasan, rating atau bintang, serta isi teks ulasan. Dalam penelitian ini, atribut utama yang digunakan untuk analisis sentimen adalah teks ulasan, sedangkan atribut lain dimanfaatkan sebagai informasi pendukung pada tahap analisis dan implementasi sistem monitoring.

Pada tahap pengumpulan dataset historis, diperoleh total 2.449 ulasan pelanggan. Data tersebut berasal dari rentang waktu 20 Februari 2020 sampai 25 Mei 2025. Dataset historis ini digunakan sebagai data eksperimen untuk proses pelabelan, preprocessing, pelatihan model, dan evaluasi performa klasifikasi sentimen.

Selain dataset historis, penelitian ini juga menggunakan data ulasan terbaru yang diambil secara periodik pada sistem operasional. Data operasional ini tidak digunakan untuk pelatihan model, melainkan untuk kebutuhan monitoring sentimen berbasis aplikasi setelah model selesai dibangun.

#### 3.2.2 Sumber Data

Sumber data pada penelitian ini dibedakan menjadi dua jenis, yaitu data historis penelitian dan data operasional sistem. Pemisahan sumber data ini dilakukan karena penelitian tidak hanya berfokus pada pembangunan model analisis sentimen, tetapi juga pada implementasi sistem monitoring ulasan yang berjalan secara periodik. Dengan demikian, setiap jenis data memiliki fungsi yang berbeda sesuai dengan kebutuhan masing-masing tahapan penelitian.

Data historis penelitian merupakan kumpulan ulasan pelanggan Aveta Hotel Malioboro yang diperoleh dari Google Maps melalui proses scraping. Data ini digunakan sebagai dataset utama dalam tahap eksperimen analisis sentimen, yang meliputi proses pelabelan, preprocessing, ekstraksi fitur, pelatihan model, serta evaluasi performa algoritma. Dengan kata lain, data historis berperan sebagai bahan dasar dalam membangun model klasifikasi sentimen yang nantinya akan diintegrasikan ke dalam sistem.

Sementara itu, data operasional sistem merupakan data ulasan terbaru yang diperoleh secara periodik melalui layanan SerpAPI pada saat aplikasi monitoring dijalankan. Data ini tidak digunakan untuk membangun model, melainkan digunakan sebagai input aktual pada sistem operasional. Ulasan terbaru yang berhasil diperoleh kemudian diproses oleh model yang telah dilatih sebelumnya untuk menghasilkan prediksi sentimen, disimpan ke dalam basis data, ditampilkan pada dashboard, dan diteruskan melalui notifikasi Telegram kepada pihak yang berkepentingan.

Pemisahan antara data historis dan data operasional ini penting secara metodologis karena menunjukkan bahwa proses pembangunan model dan proses implementasi sistem memiliki kebutuhan teknis yang berbeda. Data historis digunakan pada tahap eksperimen untuk menghasilkan model yang optimal, sedangkan data operasional digunakan pada tahap implementasi untuk mendukung fungsi monitoring ulasan pelanggan secara berkelanjutan.

### 3.3 Prosedur Pengumpulan Data

#### 3.3.1 Pengumpulan Dataset Historis

Pengumpulan dataset historis dilakukan melalui teknik web scraping terhadap ulasan pelanggan Aveta Hotel Malioboro pada Google Maps. Pada tahap ini, pendekatan yang digunakan adalah scraping berbasis browser atau *DOM scraping* untuk memperoleh kumpulan ulasan dalam jumlah besar sebagai bahan penelitian.

Proses pengumpulan dimulai dengan membuka halaman ulasan hotel pada Google Maps, kemudian memuat ulasan secara bertahap melalui mekanisme pengguliran halaman (*scrolling*) karena Google Maps menerapkan *lazy loading*. Setelah ulasan berhasil dimuat, teks ulasan diekstraksi dari elemen halaman dan disimpan ke dalam format terstruktur agar dapat diproses lebih lanjut.

Data hasil scraping historis selanjutnya dikonversi ke format yang lebih mudah diolah, seperti CSV, sehingga siap digunakan pada tahap pelabelan dan eksperimen machine learning. Pendekatan ini digunakan secara khusus untuk kebutuhan pembentukan dataset penelitian dan bukan sebagai mekanisme utama sistem operasional.

#### 3.3.2 Pengumpulan Data Operasional Sistem

Untuk mendukung sistem monitoring yang berjalan secara periodik, penelitian ini menggunakan pendekatan berbeda, yaitu pengambilan data ulasan melalui SerpAPI. Pada tahap implementasi aplikasi, penggunaan SerpAPI dipilih karena menghasilkan data yang lebih terstruktur dan lebih stabil dibanding scraping berbasis manipulasi elemen halaman secara langsung.

Melalui pendekatan ini, sistem dapat mengambil ulasan terbaru dari Google Maps secara otomatis berdasarkan `place_id` hotel. Ulasan yang diperoleh kemudian diteruskan ke pipeline klasifikasi sentimen, disimpan ke basis data, dan digunakan untuk pengiriman notifikasi. Dengan demikian, pengumpulan data operasional sistem mendukung karakter layanan aplikasi yang bersifat **near real-time** berbasis interval scheduler.

#### 3.3.3 Ringkasan Teknik Pengumpulan Data

Pada penelitian ini, teknik pengumpulan data dilakukan dengan dua pendekatan yang saling melengkapi.

1. *DOM scraping* digunakan untuk memperoleh dataset historis sebagai bahan eksperimen model.
2. SerpAPI digunakan pada sistem operasional untuk pengambilan ulasan terbaru secara periodik dan terstruktur.

Pendekatan ganda ini perlu dijelaskan secara eksplisit agar tidak menimbulkan kesan bahwa penelitian mencampur metodologi tanpa alasan. Secara akademik, pemisahan ini justru memperkuat metodologi karena menunjukkan bahwa teknik pengumpulan data disesuaikan dengan kebutuhan masing-masing tahap penelitian.

### 3.4 Aturan Bisnis

#### 3.4.1 Aturan Bisnis Sistem yang Berjalan

Pemantauan ulasan pelanggan pada Aveta Hotel Malioboro pada kondisi awal masih dilakukan secara manual melalui platform Google Maps. Ulasan yang masuk akan tersimpan pada halaman ulasan hotel dan dapat diakses oleh pihak pengelola melalui akun Google yang terdaftar. Untuk mengetahui adanya ulasan baru, pihak manajemen harus membuka halaman Google Maps hotel secara berkala dan membaca isi ulasan pelanggan satu per satu. Sistem yang berjalan belum dilengkapi dengan mekanisme klasifikasi sentimen, sehingga ulasan bernada positif dan negatif tidak dapat dibedakan secara sistematis. Selain itu, notifikasi ulasan umumnya hanya terhubung pada satu akun pengelola, sehingga informasi mengenai ulasan baru, termasuk ulasan bernada negatif, tidak selalu diketahui secara langsung oleh seluruh pihak yang berkepentingan.

Kondisi tersebut menjadi semakin tidak efektif ketika jumlah ulasan pelanggan terus meningkat, terutama pada periode dengan intensitas operasional hotel yang tinggi seperti akhir pekan atau jam sibuk. Dalam situasi tersebut, tidak terdapat mekanisme sistem yang secara otomatis memberikan peringatan dini terhadap ulasan baru yang memerlukan perhatian. Akibatnya, proses pemantauan sangat bergantung pada aktivitas pengecekan manual terhadap halaman Google Maps.

Berdasarkan kondisi tersebut, terdapat beberapa permasalahan utama pada sistem yang berjalan. Pertama, identifikasi ulasan bernada negatif menjadi terlambat karena tidak adanya mekanisme klasifikasi sentimen otomatis. Kedua, sistem belum menyediakan skema prioritas penanganan ulasan, sehingga ulasan negatif yang bersifat keluhan diperlakukan sama dengan ulasan positif. Ketiga, proses pemantauan sangat bergantung pada konsistensi pihak manajemen dalam melakukan pengecekan manual, yang meningkatkan risiko keterlambatan informasi. Keempat, distribusi informasi ulasan yang terbatas pada akun tertentu menyebabkan informasi ulasan baru tidak selalu diterima tepat waktu oleh seluruh pihak yang bertanggung jawab.

Dengan demikian, aturan bisnis yang berjalan masih berorientasi pada pemantauan manual dan belum mampu mendukung kebutuhan pengelolaan ulasan pelanggan secara cepat, terstruktur, dan berbasis data. Kondisi ini menunjukkan adanya kesenjangan antara kebutuhan pemantauan ulasan yang responsif dengan mekanisme yang tersedia saat ini.

#### 3.4.2 Aturan Bisnis Sistem yang Diusulkan

Berdasarkan permasalahan pada sistem yang berjalan, diusulkan aturan bisnis baru berupa sistem monitoring sentimen ulasan pelanggan yang bekerja secara otomatis. Dalam aturan bisnis yang diusulkan, ulasan terbaru diambil secara periodik dari Google Maps, kemudian diproses menggunakan model analisis sentimen untuk mengklasifikasikan isi ulasan ke dalam kategori positif atau negatif. Hasil klasifikasi tersebut selanjutnya disimpan dalam basis data dan ditampilkan pada dashboard monitoring.

Apabila sistem mendeteksi adanya ulasan baru, informasi tersebut dapat diteruskan kepada subscriber melalui Telegram Bot sebagai media notifikasi otomatis. Dengan mekanisme ini, pihak manajemen hotel tidak perlu lagi memantau Google Maps secara manual untuk mengetahui adanya ulasan baru. Selain itu, data ulasan yang telah diproses akan tersimpan secara historis sehingga dapat digunakan untuk kebutuhan analisis lanjutan.

Secara umum, aturan bisnis yang diusulkan terdiri atas tiga kondisi utama. Pada kondisi awal, ulasan pelanggan masih dipantau secara manual melalui Google Maps. Pada proses sistem yang diusulkan, aplikasi melakukan scraping berkala, klasifikasi sentimen, penyimpanan data, visualisasi hasil, dan pengiriman notifikasi. Pada kondisi akhir, pihak manajemen hotel memperoleh informasi ulasan secara lebih cepat, terstruktur, dan berbasis data melalui sistem monitoring yang terintegrasi.

Dengan demikian, aturan bisnis yang diusulkan tidak lagi menempatkan proses pemantauan ulasan sebagai aktivitas manual, melainkan sebagai proses otomatis yang didukung oleh pengambilan data, analisis sentimen, penyimpanan historis, dan distribusi informasi secara terintegrasi. Dalam konteks implementasi, karakter layanan sistem ini lebih tepat disebut **near real-time**, karena pembaruan informasi bergantung pada interval scheduler, bukan pada aliran data yang berlangsung secara kontinu.

### 3.5 Tahapan Penelitian

Tahapan penelitian disusun secara sistematis agar seluruh proses dapat dilaksanakan secara terukur dan dapat dipertanggungjawabkan secara ilmiah. Tahapan penelitian pada studi ini meliputi identifikasi masalah, studi literatur, pengumpulan data, pelabelan data, preprocessing, ekstraksi fitur, pelatihan model, evaluasi model, implementasi sistem, dan pengujian sistem.

#### 3.5.1 Identifikasi Masalah

Tahap awal penelitian diawali dengan identifikasi permasalahan yang terjadi pada proses pemantauan ulasan pelanggan di Aveta Hotel Malioboro. Permasalahan utama yang diidentifikasi adalah belum tersedianya sistem pemantauan ulasan Google Maps yang mampu mengklasifikasikan sentimen ulasan secara otomatis dan near real-time, serta memberikan notifikasi dini kepada manajemen hotel terhadap ulasan baru, terutama yang bernada negatif. Identifikasi masalah dilakukan berdasarkan pengamatan terhadap proses bisnis yang berjalan serta kajian terhadap kebutuhan manajemen hotel dalam merespons ulasan pelanggan secara cepat.

Hasil identifikasi masalah ini menjadi dasar perumusan tujuan penelitian, yaitu membangun sistem monitoring sentimen ulasan hotel berbasis web yang terintegrasi dengan analisis sentimen dan notifikasi otomatis.

#### 3.5.2 Studi Literatur

Tahap selanjutnya adalah studi literatur yang bertujuan untuk memperoleh landasan teoritis dan metodologis yang relevan dengan penelitian. Studi literatur dilakukan dengan menelaah jurnal ilmiah, buku referensi, dokumentasi teknis, dan penelitian terdahulu yang berkaitan dengan:

1. analisis sentimen,
2. text preprocessing,
3. TF-IDF,
4. Naive Bayes,
5. Support Vector Machine,
6. monitoring ulasan pelanggan,
7. integrasi sistem berbasis web dan notifikasi.

Hasil studi literatur digunakan sebagai dasar dalam pemilihan metode pengolahan teks, algoritma klasifikasi, pendekatan evaluasi model, dan rancangan sistem yang diusulkan.

#### 3.5.3 Pengumpulan Data

Pada tahap ini dilakukan pengumpulan data ulasan pelanggan Aveta Hotel Malioboro dari Google Maps. Pengumpulan data dibagi ke dalam dua kebutuhan utama, yaitu pengumpulan data historis untuk kebutuhan eksperimen model dan pengumpulan data terbaru untuk kebutuhan monitoring operasional sistem. Data historis digunakan sebagai dataset penelitian untuk proses pelatihan dan evaluasi model analisis sentimen, sedangkan data terbaru digunakan pada saat sistem dijalankan untuk mendeteksi ulasan baru secara periodik.

#### 3.5.4 Pelabelan Data

Setelah dataset historis diperoleh, tahap berikutnya adalah pelabelan data sentimen. Pada penelitian ini, pelabelan dilakukan menggunakan model transformer pra-latih bahasa Indonesia, yaitu model klasifikasi sentimen berbasis RoBERTa. Pendekatan ini digunakan untuk menghasilkan label sentimen positif dan negatif secara konsisten terhadap dataset yang telah dikumpulkan, sehingga data siap digunakan sebagai dasar pembentukan model klasifikasi.

Secara metodologis, pelabelan ini termasuk kategori *weak supervision* karena label referensi tidak berasal dari anotasi manual penuh oleh manusia. Oleh karena itu, tahap ini perlu dijelaskan secara jujur dalam laporan agar pembaca memahami bahwa kualitas label tetap memiliki keterbatasan.

#### 3.5.5 Preprocessing Data

Data ulasan yang telah dilabeli kemudian diproses melalui tahap preprocessing untuk meningkatkan kualitas data sebelum dilakukan ekstraksi fitur dan klasifikasi. Tahapan preprocessing pada penelitian ini meliputi:

1. *case folding*,
2. *cleaning*,
3. tokenisasi,
4. normalisasi kata,
5. stopword removal,
6. stemming.

Tahapan ini bertujuan untuk menghilangkan *noise*, menyeragamkan bentuk kata, dan menghasilkan representasi teks yang lebih sesuai untuk proses klasifikasi sentimen.

#### 3.5.6 Ekstraksi Fitur TF-IDF

Setelah preprocessing selesai, data teks diubah ke dalam bentuk numerik menggunakan metode *Term Frequency-Inverse Document Frequency* (TF-IDF). Metode ini digunakan untuk merepresentasikan bobot kata berdasarkan frekuensi kemunculannya dalam dokumen dan tingkat kepentingannya terhadap keseluruhan korpus.

Hasil ekstraksi fitur TF-IDF menjadi masukan utama bagi model klasifikasi sentimen. Pada eksperimen penelitian ini, ukuran kosakata TF-IDF yang terbentuk adalah 5.123 fitur.

#### 3.5.7 Pelatihan Model Klasifikasi

Tahap pelatihan model klasifikasi dilakukan dengan menerapkan dua algoritma machine learning, yaitu Naive Bayes dan Support Vector Machine. Dalam eksperimen akhir penelitian, pendekatan Naive Bayes yang digunakan mengarah pada keluarga *Complement Naive Bayes*, sedangkan model SVM diimplementasikan menggunakan *Linear SVM*. Kedua algoritma digunakan untuk mengklasifikasikan ulasan pelanggan ke dalam kategori sentimen positif dan negatif.

Data dibagi menjadi data latih dan data uji dengan rasio 80:20. Selanjutnya, pelatihan dan optimasi parameter dilakukan pada dua skenario:

1. skenario tidak seimbang, yaitu distribusi data latih dibiarkan sesuai kondisi awal, dan
2. skenario seimbang, yaitu data latih diseimbangkan melalui proses *resample* pada kelas minoritas.

Penerapan dua skenario ini bertujuan untuk melihat pengaruh distribusi kelas terhadap performa model dan memberikan dasar pembandingan yang lebih objektif dalam konteks analisis sentimen ulasan hotel pada Google Maps.

#### 3.5.8 Evaluasi Model

Model yang telah dilatih selanjutnya dievaluasi untuk mengukur tingkat kinerjanya. Evaluasi tidak hanya menggunakan accuracy, tetapi juga melibatkan precision weighted, recall weighted, F1-score weighted, F1-score macro, dan balanced accuracy. Untuk model Naive Bayes dihitung pula log loss, sedangkan untuk model SVM dihitung hinge loss.

Penggunaan banyak metrik pada tahap evaluasi penting untuk menghindari kesimpulan yang terlalu sederhana. Hal ini terutama relevan ketika distribusi kelas data tidak sepenuhnya seimbang, sehingga accuracy saja tidak cukup untuk menggambarkan kualitas model secara menyeluruh. Hasil evaluasi ini digunakan sebagai dasar untuk menentukan model yang paling sesuai untuk diimplementasikan dalam sistem monitoring.

#### 3.5.9 Implementasi Sistem Monitoring

Setelah model terbaik diperoleh, model diintegrasikan ke dalam sistem monitoring ulasan pelanggan berbasis web. Sistem dibangun menggunakan Flask, MySQL/MariaDB, APScheduler, SerpAPI, dan Telegram Bot API.

Pada tahap ini, sistem dirancang untuk:

1. mengambil ulasan terbaru secara periodik,
2. melakukan prediksi sentimen menggunakan model yang telah dilatih,
3. menyimpan hasil ke basis data,
4. menampilkan hasil pada dashboard dan halaman analitik,
5. mengirimkan notifikasi kepada subscriber Telegram.

Tahap ini penting karena menunjukkan bahwa hasil penelitian tidak berhenti pada eksperimen model, tetapi diwujudkan dalam bentuk aplikasi yang dapat digunakan dalam proses monitoring ulasan pelanggan secara operasional.

#### 3.5.10 Pengujian Sistem

Pengujian sistem dilakukan untuk memastikan bahwa seluruh komponen sistem monitoring berjalan sesuai dengan fungsi yang dirancang. Pengujian meliputi:

1. pengujian autentikasi,
2. pengujian scraping ulasan,
3. pengujian klasifikasi sentimen,
4. pengujian penyimpanan data,
5. pengujian tampilan dashboard dan analitik,
6. pengujian scheduler,
7. pengujian pengiriman notifikasi Telegram.

Tahap ini bertujuan untuk memastikan bahwa sistem mampu beroperasi secara stabil dan memberikan informasi yang akurat sesuai kebutuhan pengguna.

#### 3.5.11 Penyusunan Hasil dan Kesimpulan

Tahap akhir penelitian adalah penyusunan hasil, pembahasan, kesimpulan, dan saran berdasarkan seluruh proses dan pengujian yang telah dilakukan. Pada tahap ini, seluruh temuan dari eksperimen model dan implementasi sistem dianalisis untuk menjawab tujuan penelitian. Selain itu, keterbatasan penelitian dan peluang pengembangan lanjutan juga diidentifikasi agar penelitian memiliki nilai ilmiah yang lebih kuat.

### 3.6 Alur Umum Penelitian

Secara ringkas, alur umum penelitian ini dapat dijelaskan sebagai berikut:

1. Mengidentifikasi masalah pemantauan ulasan pelanggan yang masih manual.
2. Melakukan studi literatur untuk menentukan metode dan pendekatan penelitian.
3. Mengumpulkan dataset historis ulasan pelanggan dari Google Maps.
4. Melakukan pelabelan sentimen menggunakan model transformer pra-latih.
5. Melakukan preprocessing data teks.
6. Mengekstraksi fitur menggunakan TF-IDF.
7. Melatih dan mengevaluasi model Naive Bayes dan SVM pada dua skenario eksperimen.
8. Mengintegrasikan model ke dalam sistem monitoring berbasis web.
9. Melakukan pengujian sistem secara fungsional.
10. Menyusun hasil, pembahasan, kesimpulan, dan saran.

### 3.7 Ringkasan Bab

Bab ini menjelaskan metode penelitian yang digunakan dalam pembangunan sistem monitoring sentimen ulasan hotel. Penelitian memanfaatkan dataset historis ulasan Google Maps sebanyak 2.449 data untuk membangun dan mengevaluasi model analisis sentimen. Proses penelitian mencakup pengumpulan data, pelabelan, preprocessing, ekstraksi fitur TF-IDF, pelatihan model Naive Bayes dan SVM, evaluasi performa, integrasi model ke aplikasi, serta pengujian sistem monitoring.

Rangkaian metode tersebut dirancang agar penelitian tidak hanya menghasilkan model klasifikasi sentimen yang dapat diukur performanya, tetapi juga menghasilkan aplikasi monitoring ulasan hotel yang fungsional dan dapat digunakan secara near real-time berbasis scheduler. Tahapan metode penelitian ini menjadi landasan bagi analisis dan perancangan sistem pada bab berikutnya.
