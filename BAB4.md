## BAB IV ANALISIS DAN PERANCANGAN SISTEM

### 4.1 Analisis Sistem

#### 4.1.1 Analisis Sistem yang Berjalan

Sistem pemantauan ulasan pelanggan pada Aveta Hotel Malioboro saat ini masih bergantung pada fitur bawaan platform Google Maps tanpa adanya integrasi dengan sistem informasi internal hotel. Ulasan pelanggan yang diberikan melalui Google Maps hanya tersimpan pada halaman ulasan dan belum diproses lebih lanjut secara otomatis untuk kebutuhan monitoring, analisis, maupun distribusi informasi kepada manajemen hotel.

Pada kondisi tersebut, Google Maps hanya berfungsi sebagai media publikasi ulasan dan belum menyediakan mekanisme pengambilan data ulasan secara terstruktur (*data acquisition*) yang memungkinkan ulasan diproses secara komputasional. Akibatnya, data ulasan tidak dapat dimanfaatkan secara optimal untuk mendukung pengambilan keputusan manajemen. Proses identifikasi ulasan masih dilakukan secara manual dengan membaca satu per satu ulasan yang masuk. Selain itu, sistem yang berjalan tidak memiliki modul pemrosesan teks, sehingga tidak mampu melakukan klasifikasi sentimen untuk membedakan ulasan positif dan negatif. Hal ini menyebabkan tidak adanya prioritas penanganan terhadap ulasan bernada negatif yang seharusnya ditangani lebih cepat.

Keterbatasan lain dari sistem yang berjalan adalah belum tersedianya mekanisme notifikasi otomatis yang terintegrasi. Informasi mengenai ulasan baru hanya dapat diketahui apabila manajemen secara aktif membuka halaman Google Maps hotel. Kondisi ini menyebabkan keterlambatan informasi, terutama ketika volume ulasan meningkat atau saat pihak manajemen sedang berfokus pada aktivitas operasional harian. Selain itu, distribusi informasi ulasan sering kali hanya terpusat pada akun tertentu, sehingga tidak seluruh pihak yang bertanggung jawab dapat menerima informasi secara cepat dan serentak.

Secara keseluruhan, sistem yang berjalan belum mampu memenuhi kebutuhan pemantauan ulasan secara cepat, terstruktur, dan analitis. Sistem juga belum mendukung pemanfaatan sentimen berbasis data serta belum menyediakan mekanisme peringatan dini terhadap ulasan yang memerlukan perhatian segera. Keterbatasan ini menjadi dasar perlunya pengembangan sistem monitoring sentimen otomatis yang terintegrasi dengan teknik machine learning dan notifikasi.

#### 4.1.2 Analisis Sistem yang Diusulkan

Berdasarkan hasil analisis terhadap sistem yang berjalan, serta mengacu pada tujuan penelitian, diusulkan sebuah sistem monitoring sentimen ulasan hotel berbasis web yang terintegrasi dengan notifikasi Telegram. Sistem ini dirancang untuk mengatasi keterbatasan pemantauan manual dan ketiadaan klasifikasi sentimen otomatis dengan cara mengotomasi pengambilan data ulasan, klasifikasi sentimen, penyimpanan data, visualisasi hasil, dan pengiriman notifikasi.

Sistem yang diusulkan mengambil data ulasan pelanggan dari Google Maps melalui layanan pihak ketiga, yaitu SerpAPI. Penggunaan SerpAPI dipilih karena mampu menyediakan data ulasan dalam format terstruktur, sehingga lebih stabil dan mudah diproses dibanding pendekatan scraping berbasis parsing HTML secara langsung. Ulasan yang berhasil diperoleh kemudian diproses oleh sistem untuk dilakukan klasifikasi sentimen menggunakan dua algoritma machine learning, yaitu Naive Bayes dan Support Vector Machine (SVM). Kedua algoritma ini digunakan untuk mengklasifikasikan ulasan pelanggan ke dalam dua kategori sentimen, yaitu positif dan negatif. Hasil klasifikasi ini selanjutnya menjadi dasar dalam menentukan tindak lanjut terhadap ulasan yang masuk.

Hasil klasifikasi sentimen disimpan ke dalam basis data dan ditampilkan pada dashboard monitoring. Sistem juga menyediakan halaman analitik untuk melihat distribusi sentimen, tren ulasan, serta informasi pendukung lain seperti rating dan kata kunci dominan. Selain itu, sistem terintegrasi dengan Telegram Bot untuk mengirimkan notifikasi otomatis kepada subscriber ketika terdapat ulasan baru yang berhasil diproses. Dengan mekanisme ini, manajemen hotel tidak perlu lagi melakukan pengecekan manual secara berulang pada Google Maps untuk mengetahui adanya ulasan baru.

Secara konseptual, alur kerja sistem yang diusulkan dimulai ketika pelanggan memberikan ulasan melalui Google Maps. Ulasan yang masuk kemudian diambil secara otomatis melalui proses scraping berbasis API, diproses oleh sistem, disimpan dalam basis data, lalu dianalisis menggunakan algoritma Naive Bayes dan Support Vector Machine (SVM) untuk menentukan sentimen positif atau negatif. Hasil klasifikasi tersebut selanjutnya dapat dikirimkan melalui Telegram Bot sebagai notifikasi kepada pihak manajemen hotel atau subscriber terkait. Dengan alur ini, sistem memungkinkan manajemen menerima informasi ulasan terbaru beserta sentimennya secara lebih cepat, sehingga tindak lanjut terhadap ulasan pelanggan, khususnya ulasan bernada negatif, dapat dilakukan dengan lebih responsif.

Karena proses pengambilan data dilakukan secara periodik menggunakan scheduler, karakter layanan sistem ini lebih tepat disebut **near real-time**. Istilah ini lebih akurat dibanding menyatakan sistem bekerja secara real-time murni, karena pembaruan informasi tetap bergantung pada interval polling yang telah dikonfigurasi.

Secara keseluruhan, sistem yang diusulkan diharapkan mampu membantu manajemen hotel memantau ulasan pelanggan dengan lebih cepat, terstruktur, dan berbasis data, sehingga proses evaluasi layanan dapat dilakukan secara lebih efektif.

Gambar 4.1 Proses Bisnis Sistem Monitoring Sentimen yang Diusulkan

#### 4.1.3 Analisis Kebutuhan Fungsional

Kebutuhan fungsional menjelaskan fungsi dan layanan yang harus disediakan oleh sistem agar tujuan penelitian dapat tercapai. Berdasarkan analisis sistem dan implementasi yang dibangun, kebutuhan fungsional sistem meliputi:

1. Sistem harus menyediakan fitur autentikasi pengguna berupa register, login, dan logout.
2. Sistem harus dapat menghubungkan satu akun pengguna dengan satu hotel yang dimonitor.
3. Sistem harus dapat menerima `place_id` atau tautan Google Maps saat proses registrasi hotel.
4. Sistem harus dapat mengambil ulasan terbaru dari Google Maps melalui SerpAPI.
5. Sistem harus dapat mendeteksi duplikasi ulasan agar data yang sama tidak diproses berulang.
6. Sistem harus dapat melakukan klasifikasi sentimen ulasan menggunakan model Naive Bayes dan SVM.
7. Sistem harus dapat menyimpan data ulasan mentah dan hasil klasifikasi sentimen ke basis data.
8. Sistem harus dapat menampilkan ringkasan hasil monitoring pada dashboard.
9. Sistem harus dapat menyajikan analitik sentimen dalam bentuk data agregat dan tren waktu.
10. Sistem harus dapat menampilkan riwayat ulasan beserta hasil prediksi pada halaman riwayat ulasan.
11. Sistem harus dapat mengelola subscriber Telegram per hotel.
12. Sistem harus dapat mengirimkan notifikasi otomatis kepada subscriber yang terdaftar.
13. Sistem harus dapat mencatat log notifikasi yang berhasil maupun gagal dikirim.
14. Sistem harus dapat menjalankan scraping otomatis berbasis scheduler dan mendukung operasi start, stop, serta pengecekan status scheduler.
15. Sistem harus menyediakan fitur administrasi tambahan bagi akun admin, seperti pengelolaan data utama dan pengawasan multi-hotel.

#### 4.1.4 Analisis Kebutuhan Nonfungsional

Kebutuhan nonfungsional menjelaskan karakteristik pendukung yang harus dipenuhi sistem agar dapat beroperasi secara baik.

1. Kinerja
   Sistem harus mampu mengambil, memproses, dan menyimpan data ulasan secara stabil pada interval tertentu tanpa mengganggu respons aplikasi web.

2. Keandalan
   Sistem harus tetap berjalan walaupun terjadi kegagalan sementara pada layanan eksternal seperti SerpAPI atau Telegram Bot API.

3. Keamanan
   Sistem harus menerapkan autentikasi, penyimpanan password dalam bentuk hash, serta pembatasan akses data berdasarkan sesi pengguna dan `hotel_id`.

4. Skalabilitas
   Struktur data dan arsitektur sistem harus memungkinkan penambahan hotel baru tanpa mengubah alur utama sistem.

5. Usability
   Antarmuka sistem harus mudah dipahami oleh pengguna non-teknis, terutama pihak manajemen hotel.

6. Maintainability
   Struktur kode harus modular agar mudah dipelihara dan dikembangkan.

7. Integrasi
   Sistem harus dapat berkomunikasi dengan basis data, SerpAPI, dan Telegram Bot API secara terintegrasi.

#### 4.1.5 Analisis Kebutuhan Masukan, Proses, dan Luaran

1. Kebutuhan masukan

   Sistem membutuhkan beberapa masukan utama, yaitu:
   - Data ulasan historis untuk pelatihan dan evaluasi model analisis sentimen.
   - Data ulasan terbaru yang diambil secara periodik dari Google Maps melalui SerpAPI.
   - Data akun pengguna dan informasi hotel saat registrasi.
   - Data subscriber Telegram untuk keperluan distribusi notifikasi.

2. Kebutuhan proses

   Sistem melakukan serangkaian proses utama sebagai berikut:
   - Validasi dan autentikasi pengguna.
   - Resolusi `place_id` dari input hotel.
   - Pengambilan ulasan terbaru dari Google Maps.
   - Pengecekan duplikasi ulasan.
   - Transformasi teks ulasan ke representasi fitur menggunakan TF-IDF.
   - Prediksi sentimen menggunakan dua model, yaitu Naive Bayes dan SVM.
   - Penyimpanan hasil ke basis data.
   - Penyajian hasil pada dashboard dan halaman analitik.
   - Pengiriman notifikasi kepada subscriber Telegram.

3. Kebutuhan luaran

   Luaran utama sistem meliputi:
   - Label sentimen ulasan berupa POSITIF dan NEGATIF.
   - Ringkasan jumlah ulasan dan distribusi sentimen.
   - Riwayat ulasan dan hasil prediksi kedua model.
   - Grafik tren sentimen dan informasi analitik lain.
   - Notifikasi otomatis yang dikirim kepada subscriber.
   - Log pengiriman notifikasi sebagai bahan audit sistem.

### 4.2 Perancangan Sistem

Perancangan sistem pada penelitian ini disusun berdasarkan kebutuhan fungsional dan nonfungsional yang telah dianalisis sebelumnya. Sistem dirancang sebagai aplikasi web berbasis Flask yang terintegrasi dengan basis data MySQL/MariaDB, model machine learning, layanan SerpAPI, dan Telegram Bot API.

Secara konseptual, sistem terdiri atas empat lapisan utama:

1. Lapisan presentasi, yaitu antarmuka web yang digunakan pengguna untuk berinteraksi dengan sistem.
2. Lapisan aplikasi, yaitu logika bisnis pada `app.py` yang mengelola route, sesi pengguna, kontrol scheduler, dan integrasi antar modul.
3. Lapisan pipeline, yaitu modul pendukung pada folder `pipeline/` yang menangani scraping, klasifikasi sentimen, basis data, dan notifikasi.
4. Lapisan data, yaitu basis data MySQL/MariaDB yang menyimpan seluruh data operasional sistem.

#### 4.2.1 Perancangan Proses Bisnis Sistem

Alur umum sistem yang dirancang adalah sebagai berikut:

1. Pengguna melakukan registrasi akun dan mengaitkan akun tersebut dengan satu hotel.
2. Setelah login, pengguna mengakses dashboard untuk memantau kondisi ulasan hotel.
3. Sistem menjalankan scraping secara manual atau otomatis berdasarkan scheduler.
4. Ulasan terbaru diperoleh melalui SerpAPI.
5. Sistem memeriksa apakah ulasan sudah pernah disimpan sebelumnya.
6. Jika ulasan baru ditemukan, sistem melakukan klasifikasi sentimen menggunakan model Naive Bayes dan SVM.
7. Data ulasan dan hasil sentimen disimpan ke basis data.
8. Dashboard, analitik, dan riwayat ulasan diperbarui secara dinamis.
9. Sistem mengirim notifikasi ke subscriber Telegram yang terkait dengan hotel tersebut.

Alur ini menunjukkan bahwa sistem tidak hanya menjalankan fungsi klasifikasi, tetapi juga menyediakan ekosistem monitoring yang lengkap dari pengambilan data hingga distribusi informasi.

### 4.3 Perancangan Logis

Perancangan logis dilakukan untuk memodelkan perilaku sistem dari sudut pandang proses, aktor, aktivitas, dan data. Dalam penelitian ini, perancangan logis direpresentasikan melalui flowchart sistem, use case diagram, activity diagram, dan entity relationship diagram.

#### 4.3.1 Flowchart Sistem

Gambar 4.2 Flowchart Diagram Sistem Monitoring

Flowchart sistem menggambarkan alur logis dan operasional Sistem Monitoring Sentimen Ulasan Hotel secara menyeluruh, mulai dari proses awal hingga sistem menghasilkan keluaran berupa informasi monitoring sentimen dan notifikasi kepada pihak manajemen hotel. Flowchart ini disusun berdasarkan alur implementasi nyata sistem, sehingga setiap tahapan yang ditampilkan merepresentasikan proses aktual yang berjalan pada sistem. Gambar 4.2 merepresentasikan alur logika sistem monitoring sentimen dari awal hingga akhir.

Pada Gambar 4.2, proses diawali pada titik *Mulai*, yang menandakan sistem siap dijalankan. Selanjutnya, pengguna menjalankan sistem atau scheduler aktif secara otomatis untuk memulai proses pengambilan data ulasan pelanggan secara periodik. Setelah sistem aktif, dilakukan pengambilan ulasan terbaru dari Google Maps melalui layanan SerpAPI, yang memungkinkan sistem memperoleh data ulasan secara otomatis dan terstruktur.

Tahap berikutnya adalah pengecekan duplikasi ulasan, yang bertujuan untuk memastikan bahwa data ulasan yang diproses belum pernah tersimpan sebelumnya di dalam basis data. Apabila ulasan teridentifikasi sebagai duplikat, maka proses dihentikan untuk menghindari pengolahan data yang sama secara berulang, sehingga efisiensi sistem tetap terjaga. Sebaliknya, apabila ulasan merupakan data baru, sistem melanjutkan ke tahap berikutnya.

Pada tahap selanjutnya, sistem melakukan preprocessing teks ulasan, yang mencakup proses pembersihan dan normalisasi data teks agar siap digunakan dalam analisis sentimen. Data teks yang telah melalui tahap preprocessing kemudian diproses pada tahap klasifikasi sentimen menggunakan model yang telah dilatih sebelumnya, yaitu Naive Bayes dan Support Vector Machine (SVM), untuk menentukan kategori sentimen ulasan pelanggan.

Hasil klasifikasi sentimen yang diperoleh selanjutnya disimpan ke dalam basis data sistem sebagai data historis yang dapat digunakan untuk kebutuhan monitoring dan analitik lanjutan. Setelah proses penyimpanan selesai, sistem secara otomatis mengirimkan notifikasi ulasan kepada subscriber melalui Telegram Bot, khususnya untuk memberikan informasi cepat kepada pihak manajemen hotel mengenai adanya ulasan baru, terutama yang bernada negatif.

Tahap akhir dari flowchart adalah pembaruan dashboard dan halaman analitik, di mana data ulasan dan hasil klasifikasi sentimen terbaru ditampilkan dalam bentuk informasi monitoring yang dapat diakses oleh manajemen hotel. Setelah seluruh proses selesai dijalankan, alur sistem berakhir pada titik *Selesai*.

Dengan alur tersebut, flowchart ini menunjukkan bahwa sistem dirancang untuk bekerja secara otomatis, periodik, dan terintegrasi dalam memantau sentimen ulasan pelanggan hotel. Selain itu, flowchart ini juga menegaskan bahwa sistem mampu mendukung pengambilan keputusan manajemen hotel secara lebih cepat dan berbasis data melalui mekanisme monitoring sentimen yang bersifat **near real-time**.

#### 4.3.2 Use Case Diagram

Gambar 4.3 Use Case Diagram Sistem Monitoring

Use case diagram pada sistem monitoring sentimen ulasan hotel digunakan untuk menggambarkan interaksi antara aktor dengan sistem berdasarkan fungsi-fungsi utama yang tersedia. Diagram ini berfokus pada kebutuhan fungsional sistem dari sudut pandang pengguna, tanpa menampilkan detail teknis atau implementasi internal sistem. Representasi visual use case diagram ditunjukkan pada Gambar 4.3.

Berdasarkan implementasi sistem yang dikembangkan, terdapat tiga aktor utama pada diagram, yaitu **User**, **Admin**, dan **Telegram Subscriber**. User merupakan pengguna sistem web yang terhubung dengan satu hotel tertentu. Aktor ini memiliki hak akses untuk melakukan login, melihat dashboard, melihat analitik, melihat riwayat ulasan, menjalankan scraping, mengelola scheduler, mengelola subscriber, dan melihat notifikasi. Dengan hak akses tersebut, user berperan sebagai pihak yang melakukan pemantauan terhadap ulasan pelanggan pada hotel yang menjadi tanggung jawabnya.

Admin merupakan aktor dengan hak akses yang lebih luas dibanding user biasa. Selain memiliki akses terhadap fungsi umum seperti autentikasi dan pemantauan data, admin juga memiliki use case tambahan berupa akses ke dashboard admin, pengelolaan data utama, aktivasi atau deaktivasi hotel, penghapusan data tertentu, serta pengawasan terhadap proses analisis sentimen. Dengan demikian, admin tidak hanya berperan sebagai pengguna sistem, tetapi juga sebagai pengelola operasional aplikasi secara menyeluruh.

Aktor ketiga adalah Telegram Subscriber. Aktor ini tidak berinteraksi langsung dengan dashboard web, melainkan menerima informasi dari sistem dalam bentuk notifikasi Telegram. Telegram Subscriber berfungsi sebagai pihak penerima hasil monitoring, khususnya informasi mengenai ulasan baru beserta hasil analisis sentimennya. Aktor ini tidak memiliki hak untuk mengubah data maupun mengatur proses dalam sistem.

Pada Gambar 4.3 juga terlihat bahwa sistem menyediakan use case utama yang mencakup proses autentikasi, pemantauan dashboard, analitik, riwayat ulasan, scraping, pengelolaan scheduler, pengelolaan subscriber, notifikasi Telegram, serta analisis sentimen menggunakan algoritma Naive Bayes dan Support Vector Machine (SVM). Sementara itu, use case khusus admin menunjukkan adanya fungsi manajerial yang tidak dimiliki oleh user biasa, sehingga pembagian hak akses dalam sistem menjadi lebih jelas.

Secara keseluruhan, use case diagram ini menegaskan bahwa sistem dirancang tidak hanya untuk mengolah data ulasan pelanggan, tetapi juga untuk mendukung pengelolaan operasional aplikasi sesuai hak akses masing-masing aktor. Dengan adanya pemisahan peran antara user, admin, dan Telegram Subscriber, sistem dapat berjalan lebih terstruktur, aman, dan sesuai dengan kebutuhan monitoring sentimen ulasan hotel.

#### 4.3.3 Activity Diagram

Gambar 4.4 Activity Diagram Sistem Monitoring

Activity diagram menggambarkan alur aktivitas Sistem Monitoring Sentimen Ulasan Hotel dengan memisahkan tanggung jawab antara pengguna atau manajemen hotel dan sistem monitoring menggunakan konsep *swimlane*. Pemisahan ini bertujuan untuk memperjelas peran masing-masing pihak dalam menjalankan sistem. Gambar 4.4 merepresentasikan secara visual urutan aktivitas sistem secara aktual, mulai dari pengguna masuk ke aplikasi hingga sistem menampilkan hasil monitoring dan mengirimkan notifikasi.

Alur aktivitas dimulai dari *initial state*, yang menandakan awal proses sistem. Pada *swimlane* pengguna, aktivitas diawali ketika admin atau manajemen hotel melakukan login ke sistem sebagai langkah awal untuk mengakses layanan yang tersedia. Setelah proses autentikasi berhasil, pengguna diarahkan ke dashboard monitoring, yang berfungsi sebagai antarmuka utama untuk melihat ringkasan hasil monitoring sentimen ulasan hotel. Dari dashboard tersebut, pengguna dapat menjalankan proses scraping secara manual atau menunggu proses yang dipicu secara otomatis oleh scheduler.

Pada *swimlane* sistem monitoring, setelah pengguna berhasil masuk, sistem melakukan validasi kredensial dan menetapkan sesi pengguna sesuai hak akses yang dimiliki. Selanjutnya, sistem menjalankan proses pengambilan ulasan terbaru dari Google Maps melalui layanan SerpAPI. Setelah data ulasan diperoleh, sistem melakukan pengecekan untuk memastikan apakah ulasan yang diproses merupakan ulasan baru atau data yang telah tersimpan sebelumnya. Apabila ulasan terdeteksi bukan data baru, sistem hanya memperbarui tampilan dashboard dan riwayat ulasan tanpa melanjutkan ke proses berikutnya. Sebaliknya, apabila ulasan merupakan data baru, sistem melanjutkan ke tahap preprocessing teks, yaitu proses pembersihan dan normalisasi data teks agar siap dianalisis.

Tahap berikutnya adalah analisis sentimen menggunakan algoritma Naive Bayes dan Support Vector Machine (SVM) untuk menentukan kategori sentimen ulasan pelanggan. Hasil klasifikasi tersebut kemudian disimpan ke dalam basis data sebagai data historis. Setelah data tersimpan, sistem secara otomatis mengirimkan notifikasi ulasan melalui Telegram Bot, khususnya untuk memberikan informasi cepat kepada pihak manajemen hotel mengenai adanya ulasan baru. Selanjutnya, sistem memperbarui dashboard dan tampilan monitoring sehingga hasil analisis sentimen terbaru dapat langsung dilihat oleh pengguna.

Dengan alur tersebut, activity diagram ini memperlihatkan hubungan yang jelas antara tindakan pengguna dan proses internal sistem. Diagram ini juga menegaskan bahwa sistem dirancang untuk bekerja secara otomatis, terstruktur, dan berkelanjutan dalam mendukung proses monitoring sentimen ulasan pelanggan hotel.

#### 4.3.4 Entity Relationship Diagram (ERD)

Gambar 4.5 Entity Relationship Diagram (ERD) Sistem Monitoring

Entity Relationship Diagram (ERD) pada penelitian ini digunakan untuk menggambarkan struktur basis data yang mendukung sistem monitoring sentimen ulasan hotel. Setiap entitas dan relasi dirancang berdasarkan kebutuhan fungsional sistem serta implementasi nyata pada kode program. Melalui ERD, hubungan antar data pada sistem dapat dipahami secara terstruktur, mulai dari data hotel, data pengguna, data ulasan pelanggan, hasil analisis sentimen, data subscriber Telegram, hingga data notifikasi. Gambar 4.5 menunjukkan bagaimana setiap entitas dalam sistem saling terhubung satu sama lain.

Pada Gambar 4.5 terlihat bahwa entitas `hotels` menjadi pusat dari struktur data sistem karena seluruh proses monitoring berfokus pada hotel yang dimonitor. Entitas ini terhubung dengan entitas `users`, `hotel_reviews`, `telegram_users`, dan `notifications`. Pada bagian atas diagram, entitas `users` berelasi dengan `hotels` melalui relasi *mengelola*, yang menunjukkan bahwa admin atau manajemen hotel berperan sebagai pihak yang mengelola data hotel dalam sistem. Dalam implementasi sistem, setiap pengguna terhubung ke satu hotel tertentu melalui `hotel_id`, sedangkan satu hotel dapat dikaitkan dengan lebih dari satu akun pengguna sesuai kebutuhan pengelolaan.

Berdasarkan skema basis data aktual, sistem memiliki enam entitas utama, yaitu:

1. `hotels`
2. `users`
3. `hotel_reviews`
4. `sentiment_reviews`
5. `telegram_users`
6. `notifications`

Hubungan antar entitas pada sistem adalah sebagai berikut:

1. `users` berelasi dengan `hotels` melalui relasi *mengelola*.
   Relasi ini menunjukkan bahwa admin atau manajemen hotel berperan sebagai pihak yang mengelola data hotel yang dimonitor dalam sistem. Pada implementasi basis data, setiap pengguna terhubung pada satu hotel tertentu melalui `hotel_id`, sedangkan satu hotel dapat dikaitkan dengan lebih dari satu akun pengguna sesuai kebutuhan administrasi sistem.

2. `hotels` berelasi dengan `hotel_reviews` melalui relasi *memiliki*.
   Relasi ini merepresentasikan bahwa setiap hotel dapat memiliki banyak ulasan pelanggan. Ulasan tersebut diperoleh dari Google Maps melalui layanan SerpAPI dan disimpan sebagai data historis dalam sistem. Setiap ulasan hanya terkait dengan satu hotel, sehingga hubungan antar entitas bersifat satu ke banyak.

3. `hotel_reviews` berelasi dengan `sentiment_reviews` melalui relasi *dianalisis*.
   Relasi ini menunjukkan bahwa setiap ulasan pelanggan dianalisis sentimennya menggunakan dua algoritma, yaitu Naive Bayes dan Support Vector Machine (SVM). Hasil analisis tersebut disimpan dalam entitas `sentiment_reviews` sebagai bagian dari proses monitoring dan evaluasi sentimen.

4. `hotels` berelasi dengan `telegram_users` melalui relasi *memiliki*.
   Relasi ini menunjukkan bahwa satu hotel dapat memiliki beberapa subscriber Telegram yang menerima informasi monitoring dari sistem. Dengan demikian, distribusi informasi ulasan tidak hanya bergantung pada satu akun pengelola.

5. `telegram_users` berelasi dengan `notifications` melalui relasi *menerima*.
   Relasi ini menunjukkan bahwa subscriber Telegram merupakan pihak yang menerima notifikasi dari sistem. Satu subscriber dapat menerima banyak notifikasi sesuai dengan ulasan baru yang diproses pada hotel yang diikutinya.

6. `hotels` berelasi dengan `notifications` melalui relasi *terkait*.
   Relasi ini menegaskan bahwa setiap notifikasi yang dikirim tetap berada dalam lingkup hotel tertentu, sehingga distribusi informasi dapat dipetakan sesuai objek monitoring.

Pada sisi kanan diagram, entitas `hotel_reviews` terhubung ke `hotels` melalui relasi *memiliki*, kemudian dilanjutkan ke entitas `sentiment_reviews` melalui relasi *dianalisis*. Susunan ini menunjukkan bahwa ulasan pelanggan yang diperoleh dari Google Maps menjadi input utama bagi proses analisis sentimen. Pada bagian bawah diagram, entitas `telegram_users` terhubung ke `hotels` melalui relasi *memiliki*, lalu diteruskan ke entitas `notifications` melalui relasi *menerima*. Selain itu, entitas `notifications` juga dihubungkan dengan `hotels` melalui relasi *terkait*, yang menegaskan bahwa setiap notifikasi tetap berada dalam konteks hotel tertentu. Dengan susunan tersebut, Gambar 4.5 memperlihatkan bahwa seluruh proses utama sistem berpusat pada data hotel, kemudian berkembang ke data ulasan, hasil analisis, subscriber, dan distribusi notifikasi.

Selain hubungan antar entitas, Gambar 4.5 juga menampilkan atribut utama dari masing-masing entitas. Entitas `hotels` memiliki atribut seperti `hotel_id`, `hotel_name`, `address`, `place_id`, `scrape_interval`, dan `is_active`. Entitas `users` memiliki atribut `user_id`, `username`, `password`, `role`, dan `created_at`. Entitas `hotel_reviews` memiliki atribut `review_id`, `user_name`, `rating`, `review_text`, `review_date`, dan `source`. Entitas `sentiment_reviews` memiliki atribut `sentiment_id`, `sentiment_nb`, `sentiment_svm`, `source`, dan `created_at`. Entitas `telegram_users` memiliki atribut `chat_id`, `subscribed`, dan `created_at`, sedangkan entitas `notifications` memiliki atribut `notif_id`, `review_id`, `status`, dan `created_at`. Penampilan atribut tersebut bertujuan untuk memperjelas data inti yang disimpan pada setiap entitas dalam sistem.

Secara keseluruhan, ERD ini menunjukkan bahwa struktur data sistem dirancang secara sederhana, konsisten, dan sesuai dengan alur operasional aplikasi. Seluruh relasi yang ditampilkan mendukung proses utama sistem, mulai dari pengelolaan data hotel, akun pengguna, pengambilan ulasan hasil scraping, analisis sentimen, pengelolaan subscriber Telegram, hingga pencatatan log notifikasi yang dikirimkan oleh sistem.

### 4.4 Perancangan Fisik

Perancangan fisik merupakan tahap penerjemahan rancangan logis ke dalam bentuk struktur implementasi yang nyata, terutama pada skema basis data dan modul aplikasi. Pada penelitian ini, perancangan fisik difokuskan pada dua aspek utama, yaitu relasi antartabel dan struktur tabel data.

#### 4.4.1 Relasi Antartabel

Perancangan relasi antartabel bertujuan untuk menggambarkan hubungan antar data yang tersimpan dalam basis data sistem monitoring sentimen ulasan hotel. Relasi ini dirancang untuk menjaga integritas data serta mendukung proses pengolahan dan penyajian informasi secara efisien. Pada Gambar 4.6 dapat dilihat relasi antar tabel yang tersimpan di basis data.

Pada Gambar 4.6, tabel `hotels` ditempatkan sebagai tabel pusat karena hampir seluruh data operasional sistem berhubungan langsung dengan hotel yang dimonitor. Di bagian atas, tabel `users` terhubung dengan tabel `hotels`, yang menunjukkan bahwa data akun pengguna sistem disimpan dalam tabel `users`, sedangkan hotel yang menjadi lingkup aksesnya disimpan melalui foreign key `hotel_id`. Tabel `users` memiliki `user_id` sebagai primary key yang berfungsi sebagai identitas unik setiap pengguna sistem.

Tabel `hotels` menyimpan data hotel yang dimonitor, termasuk `hotel_id`, `hotel_name`, `address`, `place_id`, `scrape_interval_minutes`, dan status aktif hotel. Relasi antara tabel `hotels` dan tabel lain menunjukkan bahwa satu hotel dapat menjadi induk bagi banyak data operasional, seperti data pengguna, ulasan, subscriber Telegram, hasil analisis sentimen, dan notifikasi.

Tabel `hotel_reviews` digunakan untuk menyimpan data ulasan pelanggan hotel yang diperoleh dari Google Maps melalui layanan SerpAPI. Tabel ini memiliki `review_id` sebagai primary key dan `hotel_id` sebagai foreign key yang menghubungkan ulasan dengan hotel terkait. Relasi antara tabel `hotels` dan `hotel_reviews` bersifat one-to-many, karena satu hotel dapat memiliki banyak ulasan pelanggan.

Tabel `sentiment_reviews` berfungsi untuk menyimpan hasil analisis sentimen dari setiap ulasan pelanggan. Tabel ini memiliki `sentiment_id` sebagai primary key, `review_id` sebagai foreign key yang menghubungkannya dengan tabel `hotel_reviews`, serta `hotel_id` sebagai foreign key yang menghubungkannya langsung dengan tabel `hotels`. Dengan demikian, setiap hasil klasifikasi sentimen dapat ditelusuri baik ke ulasan asalnya maupun ke hotel yang dimonitor. Relasi ini juga menunjukkan bahwa setiap ulasan dianalisis menggunakan algoritma Naive Bayes dan Support Vector Machine (SVM), sehingga hasil analisis disimpan sebagai data sentimen untuk keperluan monitoring dan evaluasi.

Di bagian bawah diagram, tabel `telegram_users` digunakan untuk menyimpan data pengguna Telegram yang berlangganan notifikasi sistem. Tabel ini menggunakan primary key komposit `chat_id` dan `hotel_id`, sehingga satu akun Telegram dapat terdaftar pada lebih dari satu hotel apabila diperlukan. Relasi antara `hotels` dan `telegram_users` menunjukkan bahwa satu hotel dapat memiliki banyak subscriber Telegram.

Tabel `notifications` menyimpan data pengiriman notifikasi yang dikirimkan oleh sistem melalui Telegram Bot. Tabel ini memiliki `notif_id` sebagai primary key serta `review_id`, `chat_id`, dan `hotel_id` sebagai foreign key yang menghubungkan notifikasi dengan ulasan, subscriber Telegram, dan hotel terkait. Pada diagram juga terlihat bahwa tabel `notifications` berelasi dengan `hotel_reviews` secara opsional karena `review_id` dapat bernilai `NULL` pada kondisi tertentu. Selain itu, relasi antara `telegram_users` dan `notifications` menunjukkan bahwa satu subscriber dapat menerima banyak notifikasi, sedangkan relasi antara `hotels` dan `notifications` menegaskan bahwa setiap notifikasi tetap berada dalam konteks hotel tertentu.

Secara keseluruhan, perancangan relasi antartabel ini memastikan bahwa alur data mulai dari pengambilan ulasan, analisis sentimen, pengelolaan subscriber, hingga pengiriman notifikasi dapat berjalan secara terintegrasi, konsisten, dan mudah ditelusuri dalam basis data.

#### 4.4.2 Perancangan Tabel Data

Perancangan tabel data dilakukan untuk menjelaskan struktur rinci dari setiap tabel yang digunakan dalam basis data sistem monitoring sentimen ulasan hotel. Masing-masing tabel disusun berdasarkan kebutuhan data pada proses autentikasi pengguna, pengelolaan hotel, penyimpanan ulasan, hasil analisis sentimen, data subscriber Telegram, serta log pengiriman notifikasi. Dengan rancangan tabel yang jelas, sistem dapat menyimpan dan mengelola data secara konsisten sesuai kebutuhan operasional aplikasi.

##### A. Tabel `users`

Tabel `users` digunakan untuk menyimpan akun pengguna sistem yang dapat melakukan login ke aplikasi. Tabel ini mendukung proses autentikasi serta pembatasan akses data berdasarkan hotel yang terhubung dengan masing-masing akun pengguna.

| Field | Tipe Data | Key | Keterangan |
|---|---|---|---|
| user_id | INT | Primary | Identitas unik pengguna |
| username | VARCHAR(100) | Unique | Nama pengguna untuk login |
| password | VARCHAR(255) |  | Password yang telah di-hash |
| role | ENUM('admin','user') |  | Peran pengguna dalam sistem |  
| created_at | TIMESTAMP |  | Waktu pembuatan akun |
| hotel_id | INT | Foreign | Relasi ke hotel yang dikelola |

##### B. Tabel `hotels`

Tabel `hotels` digunakan untuk menyimpan data hotel yang menjadi objek monitoring. Tabel ini berperan sebagai tabel utama karena terhubung dengan hampir seluruh data operasional sistem.

| Field | Tipe Data | Key | Keterangan |
|---|---|---|---|
| hotel_id | INT | Primary | Identitas unik hotel |
| manajemen_hotel_id | INT | Unique | Kode manajemen hotel |
| hotel_name | VARCHAR(255) |  | Nama hotel |
| address | VARCHAR(500) |  | Alamat hotel |
| place_id | VARCHAR(255) | Unique | Identitas Google Maps |
| created_at | TIMESTAMP |  | Waktu pembuatan data |
| scrape_interval_minutes | INT |  | Interval scraping |
| last_scrape_at | DATETIME |  | Waktu scraping terakhir |
| is_active | TINYINT(1) |  | Status hotel aktif atau tidak |

##### C. Tabel `hotel_reviews`

Tabel `hotel_reviews` digunakan untuk menyimpan data ulasan mentah yang diperoleh dari Google Maps. Tabel ini berfungsi sebagai penyimpanan awal hasil scraping sebelum ulasan diproses lebih lanjut dalam tahap analisis sentimen.

| Field | Tipe Data | Key | Keterangan |
|---|---|---|---|
| review_id | INT | Primary | Identitas unik ulasan |
| hotel_id | INT | Foreign | Relasi ke tabel hotel |
| user_name | VARCHAR(255) |  | Nama pemberi ulasan |
| review_text | TEXT |  | Isi ulasan |
| rating | INT |  | Nilai rating ulasan |
| review_date | DATETIME |  | Waktu ulasan |
| source | VARCHAR(50) |  | Sumber data ulasan |
| created_at | TIMESTAMP |  | Waktu data disimpan |

##### D. Tabel `sentiment_reviews`

Tabel `sentiment_reviews` menyimpan hasil klasifikasi sentimen yang dihasilkan sistem. Data pada tabel ini merupakan hasil pengolahan dari tabel `hotel_reviews`, sehingga tabel ini menjadi pusat data analitik untuk monitoring sentimen.

| Field | Tipe Data | Key | Keterangan |
|---|---|---|---|
| sentiment_id | INT | Primary | Identitas unik hasil sentimen |
| review_id | INT | Foreign | Relasi ke tabel ulasan |
| hotel_id | INT | Foreign | Relasi ke tabel hotel |
| user_name | VARCHAR(255) |  | Nama pemberi ulasan |
| review_text | TEXT |  | Isi ulasan |
| rating | TINYINT UNSIGNED |  | Nilai rating |
| review_date | DATETIME |  | Waktu ulasan |
| sentiment_nb | VARCHAR(50) |  | Hasil prediksi Naive Bayes |
| sentiment_svm | VARCHAR(50) |  | Hasil prediksi SVM |
| source | VARCHAR(50) |  | Sumber data |
| created_at | TIMESTAMP |  | Waktu analisis disimpan |

##### E. Tabel `telegram_users`

Tabel `telegram_users` digunakan untuk menyimpan data subscriber Telegram yang menerima notifikasi dari sistem. Tabel ini memastikan bahwa proses distribusi informasi dapat diarahkan kepada subscriber sesuai hotel yang dipantau.

| Field | Tipe Data | Key | Keterangan |
|---|---|---|---|
| chat_id | BIGINT | Primary | Identitas akun Telegram |
| hotel_id | INT | Primary, Foreign | Relasi ke hotel |
| subscribed | TINYINT(1) |  | Status berlangganan |
| created_at | TIMESTAMP |  | Waktu pendaftaran subscriber |

##### F. Tabel `notifications`

Tabel `notifications` digunakan untuk menyimpan log pengiriman notifikasi. Tabel ini berfungsi sebagai catatan historis pengiriman pesan yang dilakukan oleh sistem melalui Telegram Bot.

| Field | Tipe Data | Key | Keterangan |
|---|---|---|---|
| notif_id | INT | Primary | Identitas unik notifikasi |
| review_id | INT | Foreign | Relasi ke ulasan terkait |
| chat_id | BIGINT | Foreign | Relasi ke subscriber Telegram |
| hotel_id | INT | Foreign | Relasi ke hotel |
| status | VARCHAR(50) |  | Status pengiriman notifikasi |
| created_at | TIMESTAMP |  | Waktu notifikasi dicatat |

### 4.5 Perancangan Arsitektur Aplikasi

Arsitektur aplikasi yang dirancang dalam penelitian ini mengadopsi pola modular agar memudahkan pengembangan dan pemeliharaan sistem. Komponen utamanya adalah sebagai berikut:

1. `app.py`
   Bertanggung jawab terhadap route halaman, route API, autentikasi, sesi pengguna, kontrol scheduler, dan kontrol bot.

2. `pipeline/mysql_connector.py`
   Bertanggung jawab mengelola akses basis data, query penyimpanan, query analitik, pengelolaan subscriber, dan log notifikasi.

3. `pipeline/scraper.py`
   Bertanggung jawab mengambil ulasan terbaru dari Google Maps melalui SerpAPI.

4. `pipeline/model_predict.py`
   Bertanggung jawab memuat model machine learning dan menghasilkan prediksi sentimen.

5. `pipeline/place_id.py`
   Bertanggung jawab mengekstrak dan memvalidasi `place_id` dari input pengguna.

6. `templates/` dan `static/`
   Bertanggung jawab menyajikan antarmuka sistem kepada pengguna.

Gambar 4.7 Arsitektur Aplikasi Sistem Monitoring Sentimen

Pada Gambar 4.7, arsitektur aplikasi dibagi ke dalam beberapa komponen yang saling terhubung. Interaksi pengguna dimulai dari browser web, yang mengakses antarmuka sistem melalui halaman-halaman yang dibangun menggunakan `templates/` dan `static/`. Permintaan dari pengguna kemudian diproses oleh `app.py` sebagai pusat logika aplikasi. Modul ini bertanggung jawab mengelola route halaman, route API, autentikasi, sesi pengguna, kontrol scheduler, serta koordinasi antar modul pendukung.

Setelah menerima permintaan dari pengguna atau trigger otomatis dari scheduler, aplikasi akan berinteraksi dengan modul-modul pada folder `pipeline/`. Modul `scraper.py` bertugas mengambil ulasan terbaru dari Google Maps melalui SerpAPI. Modul `place_id.py` digunakan untuk mengekstrak dan memvalidasi `place_id` dari input pengguna saat proses awal pengaturan hotel. Selanjutnya, `model_predict.py` memuat model machine learning dan vectorizer yang telah disimpan sebelumnya untuk menghasilkan prediksi sentimen terhadap ulasan yang diperoleh. Hasil prediksi, data ulasan, data subscriber, dan log notifikasi kemudian dikelola melalui `mysql_connector.py` yang menjadi penghubung utama dengan basis data MySQL/MariaDB.

Pada sisi distribusi informasi, sistem juga terintegrasi dengan Telegram Bot API. Integrasi ini memungkinkan hasil monitoring ulasan yang telah diproses dikirimkan secara otomatis kepada subscriber Telegram yang terdaftar. Dengan demikian, arsitektur tidak hanya mendukung proses pengambilan dan analisis data, tetapi juga mendukung penyampaian informasi secara langsung kepada pengguna yang berkepentingan.

Arsitektur modular ini dipilih karena memberikan pemisahan tanggung jawab yang jelas antara logika aplikasi, akses data, proses scraping, inferensi model, dan tampilan antarmuka. Pendekatan ini memudahkan pengembangan lanjutan, pemeliharaan sistem, serta pengujian setiap komponen secara terpisah tanpa mengganggu keseluruhan alur aplikasi.

### 4.6 Ringkasan Bab

Bab ini menjelaskan analisis dan perancangan sistem monitoring sentimen ulasan hotel berbasis web yang diusulkan pada penelitian. Hasil analisis menunjukkan bahwa sistem yang berjalan masih bersifat manual dan belum mendukung pengolahan data ulasan secara otomatis. Oleh karena itu, dirancang sistem baru yang mampu melakukan scraping ulasan melalui SerpAPI, klasifikasi sentimen menggunakan Naive Bayes dan SVM, penyimpanan data ke basis data, visualisasi hasil melalui dashboard, serta pengiriman notifikasi ke subscriber Telegram.

Perancangan sistem dilakukan melalui analisis kebutuhan, pemodelan logis, perancangan fisik basis data, dan perancangan arsitektur aplikasi. Seluruh rancangan tersebut menjadi landasan implementasi sistem yang dibahas pada bab berikutnya.
