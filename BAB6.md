## ABSTRAK

Ulasan pelanggan pada Google Maps merupakan salah satu sumber informasi penting yang dapat memengaruhi citra dan reputasi hotel. Peningkatan jumlah ulasan yang masuk secara terus-menerus menimbulkan kendala bagi manajemen hotel dalam melakukan pemantauan secara manual, khususnya dalam mengidentifikasi ulasan bernada negatif yang memerlukan respons cepat. Penelitian ini bertujuan untuk merancang dan mengimplementasikan sistem monitoring sentimen ulasan pelanggan pada Aveta Hotel Malioboro berbasis web yang terintegrasi dengan analisis sentimen dan notifikasi Telegram.
Data penelitian berupa 2.449 ulasan historis pelanggan yang diperoleh dari Google Maps melalui teknik *DOM scraping*. Tahapan penelitian meliputi pengumpulan data, pelabelan sentimen, *preprocessing* teks, ekstraksi fitur menggunakan TF-IDF, pelatihan dan evaluasi model klasifikasi, serta implementasi sistem monitoring. Metode klasifikasi sentimen yang digunakan adalah Naive Bayes dan Support Vector Machine (SVM). 
Hasil penelitian menunjukkan bahwa model Support Vector Machine pada skenario penyeimbangan data latih memberikan performa terbaik dengan nilai *accuracy* sebesar 0,9540, *F1-score weighted* sebesar 0,9522, dan *F1-score macro* sebesar 0,8405. Adapun nilai *balanced accuracy* tertinggi diperoleh model Support Vector Machine pada skenario data latih tidak seimbang, yaitu sebesar 0,8950. Model terbaik selanjutnya diintegrasikan ke dalam sistem monitoring yang mampu mengambil ulasan terbaru secara periodik melalui SerpAPI, mengklasifikasikan sentimen secara otomatis, menyimpan hasil ke basis data, menyajikan informasi pada dashboard, dan mengirimkan notifikasi melalui Telegram Bot. Dengan demikian, sistem yang dibangun mampu mendukung pemantauan ulasan pelanggan secara lebih cepat, terstruktur, dan berbasis data dalam pola layanan *near real-time*.

**Kata kunci:** analisis sentimen, Google Maps, Naive Bayes, Support Vector Machine, monitoring ulasan, *near real-time*

## ABSTRACT

Customer reviews on Google Maps constitute an important source of information that can influence a hotel's image and reputation. The continuous increase in the number of incoming reviews creates challenges for hotel management in conducting manual monitoring, particularly in identifying negative reviews that require a prompt response. This study aims to design and implement a web-based customer review sentiment monitoring system for Aveta Hotel Malioboro integrated with sentiment analysis and Telegram notifications.

The research data consisted of 2,449 historical customer reviews collected from Google Maps using the *DOM scraping* technique. The research stages included data collection, sentiment labeling, text preprocessing, feature extraction using TF-IDF, training and evaluation of classification models, and implementation of the monitoring system. The sentiment classification methods used in this study were Naive Bayes and Support Vector Machine (SVM).

The results showed that the Support Vector Machine model in the balanced training data scenario achieved the best performance, with an *accuracy* of 0.9540, a *weighted F1-score* of 0.9522, and a *macro F1-score* of 0.8405. Meanwhile, the highest *balanced accuracy*, 0.8950, was obtained by the Support Vector Machine model in the imbalanced training data scenario. The selected best model was then integrated into a monitoring system capable of periodically retrieving the latest reviews through SerpAPI, automatically classifying sentiment, storing the results in a database, presenting information on a dashboard, and sending notifications via a Telegram Bot. Therefore, the developed system is able to support customer review monitoring in a faster, more structured, and data-driven manner within a *near real-time* service pattern.

## BAB VI
## PENUTUP

### 6.1 Simpulan

Berdasarkan hasil penelitian dan pembahasan yang telah dilakukan, simpulan penelitian ini adalah sebagai berikut.

1. Perbandingan performa algoritma Naive Bayes dan Support Vector Machine (SVM) menunjukkan bahwa kedua algoritma dapat digunakan untuk mengklasifikasikan sentimen ulasan Google Maps ke dalam kategori positif dan negatif. Namun demikian, keduanya memiliki karakteristik performa yang berbeda. Pada skenario data latih seimbang, model SVM memberikan nilai *accuracy* tertinggi sebesar 0,9540, sedangkan pada skenario data latih tidak seimbang, model SVM memberikan nilai *balanced accuracy* tertinggi sebesar 0,8950. Hasil tersebut menunjukkan bahwa SVM memiliki performa yang lebih stabil dan lebih layak digunakan pada sistem monitoring sentimen yang dikembangkan.

2. Penelitian ini berhasil membangun model analisis sentimen berbasis TF-IDF dan *machine learning* untuk mengklasifikasikan ulasan hotel ke dalam dua kategori, yaitu POSITIF dan NEGATIF. Proses yang dilakukan meliputi pengumpulan data historis, pelabelan data, preprocessing, pembentukan fitur TF-IDF, pembagian data latih dan data uji, serta evaluasi model pada dua skenario eksperimen. Hasil tersebut menunjukkan bahwa kombinasi TF-IDF dengan algoritma *machine learning* klasik masih efektif untuk analisis sentimen teks berbahasa Indonesia pada domain ulasan hotel.

3. Penelitian ini berhasil merancang dan mengimplementasikan sistem monitoring ulasan hotel berbasis web yang terintegrasi dengan model analisis sentimen. Sistem yang dikembangkan mampu melakukan pengambilan ulasan terbaru melalui SerpAPI, klasifikasi sentimen, penyimpanan hasil ke basis data, serta penyajian informasi melalui dashboard, halaman analitik, riwayat ulasan, subscriber, dan notifikasi. Dengan demikian, kebutuhan terhadap sistem monitoring ulasan yang terstruktur dan terintegrasi dapat dipenuhi.

4. Integrasi Telegram Bot sebagai media notifikasi otomatis terhadap ulasan baru berhasil diimplementasikan pada sistem. Melalui integrasi tersebut, hasil monitoring dapat didistribusikan kepada subscriber yang terdaftar secara lebih cepat dan terstruktur. Secara teknis, sistem bekerja dalam pola *near real-time* berbasis scheduler, sehingga tetap relevan untuk mendukung kebutuhan monitoring berkala pada lingkungan operasional hotel.

5. Berdasarkan keseluruhan hasil tersebut, dapat dinyatakan bahwa seluruh rumusan masalah dan tujuan penelitian telah terjawab dan tercapai. Penelitian ini tidak hanya menghasilkan model analisis sentimen, tetapi juga menghasilkan sistem monitoring yang dapat digunakan secara operasional untuk membantu manajemen hotel dalam memantau ulasan pelanggan secara lebih cepat, terstruktur, dan berbasis data.

### 6.2 Saran

Berdasarkan hasil penelitian yang telah dilakukan, saran untuk pengembangan selanjutnya adalah sebagai berikut.

1. Dataset penelitian perlu diperluas dengan menambahkan ulasan dari hotel lain atau dari platform ulasan lain agar model memiliki kemampuan generalisasi yang lebih baik.

2. Proses pelabelan data dapat ditingkatkan melalui anotasi manual atau validasi oleh lebih dari satu penilai agar kualitas label sentimen yang digunakan pada proses pelatihan menjadi lebih akurat.

3. Penelitian selanjutnya dapat membandingkan metode yang digunakan pada penelitian ini dengan pendekatan lain, seperti *deep learning* atau *transformer-based classifier*, untuk mengetahui kemungkinan peningkatan performa klasifikasi.

4. Sistem dapat dikembangkan agar memiliki mekanisme pembaruan data yang lebih cepat apabila tersedia dukungan integrasi data yang lebih real-time dari sumber eksternal.

5. Pengembangan berikutnya dapat menambahkan evaluasi dari sisi performa aplikasi, skalabilitas sistem, dan pengalaman pengguna agar sistem tidak hanya baik dari sisi akurasi model, tetapi juga kuat dari sisi implementasi operasional.

6. Fitur analitik dapat diperluas dengan penambahan visualisasi yang lebih mendalam, seperti analisis topik ulasan, tren kata kunci, atau deteksi sentimen netral, sehingga informasi yang dihasilkan menjadi lebih kaya untuk mendukung pengambilan keputusan.
