## Perhitungan Lengkap Analisis Sentimen

Dokumen ini merangkum perhitungan matematis dan numerik yang digunakan pada proyek TA, mulai dari data mentah, pembersihan data, pembagian data, pembobotan TF-IDF, penyeimbangan kelas dengan *resample*, pelatihan model Naive Bayes dan SVM, hingga evaluasi hasil.

Supaya tetap jujur secara teknis, dokumen ini menuliskan seluruh rumus, seluruh parameter, seluruh distribusi data, dan seluruh hasil numerik utama yang dipakai proyek. Namun, bobot individual untuk seluruh 5.123 fitur TF-IDF tidak dituliskan satu per satu di sini karena nilainya tersimpan di artefak model hasil pelatihan.

## 1. Data Mentah dan Data Akhir

### 1.1 Data mentah

Jumlah data historis hasil pengambilan awal:

\[
N_{mentah} = 2449
\]

### 1.2 Data akhir yang dipakai eksperimen

Setelah proses pembersihan data dan penyesuaian dataset untuk eksperimen, jumlah data yang digunakan pada tahap pemodelan adalah:

\[
N = 2175
\]

### 1.3 Distribusi kelas pada data akhir

Jumlah data per kelas:

\[
N_{positif} = 1990
\]

\[
N_{negatif} = 185
\]

Persentase kelas:

\[
\%Positif = \frac{1990}{2175} \times 100 = 91{,}4943\%
\]

\[
\%Negatif = \frac{185}{2175} \times 100 = 8{,}5057\%
\]

Ini menunjukkan bahwa dataset bersifat tidak seimbang karena kelas positif jauh lebih besar daripada kelas negatif.

## 2. Pembagian Data Latih dan Data Uji

Rasio pembagian data:

\[
80\% : 20\%
\]

### 2.1 Jumlah data latih

\[
N_{latih} = 0{,}8 \times 2175 = 1740
\]

### 2.2 Jumlah data uji

\[
N_{uji} = 0{,}2 \times 2175 = 435
\]

### 2.3 Distribusi kelas pada data latih

\[
N_{latih,positif} = 1592
\]

\[
N_{latih,negatif} = 148
\]

Persentase:

\[
\%Positif_{latih} = \frac{1592}{1740} \times 100 = 91{,}4943\%
\]

\[
\%Negatif_{latih} = \frac{148}{1740} \times 100 = 8{,}5057\%
\]

### 2.4 Distribusi kelas pada data uji

\[
N_{uji,positif} = 398
\]

\[
N_{uji,negatif} = 37
\]

Persentase:

\[
\%Positif_{uji} = \frac{398}{435} \times 100 = 91{,}4943\%
\]

\[
\%Negatif_{uji} = \frac{37}{435} \times 100 = 8{,}5057\%
\]

Karena pembagian dilakukan dengan `stratify=y`, proporsi kelas pada data latih dan data uji tetap sama dengan proporsi data keseluruhan.

## 3. Prior Kelas

Prior kelas untuk skenario data asli dihitung dari data latih:

\[
P(Positif) = \frac{1592}{1740} = 0{,}914943
\]

\[
P(Negatif) = \frac{148}{1740} = 0{,}085057
\]

Prior ini menunjukkan bahwa sebelum model melihat fitur teks, peluang awal dokumen berada pada kelas positif sudah jauh lebih besar.

## 4. Pembobotan TF-IDF

Representasi fitur teks menggunakan `TfidfVectorizer` dengan parameter:

- `tokenizer=lambda x: x` atau `identity`
- `preprocessor=lambda x: x` atau `identity`
- `token_pattern=None`
- `lowercase=False`
- `ngram_range=(1, 3)`
- `max_df=0.9`
- `min_df=2`
- `sublinear_tf=True`
- `norm='l2'`

Ukuran kosakata akhir:

\[
|V| = 5123
\]

### 4.1 Term Frequency

Frekuensi term:

\[
TF(t,d) = f(t,d)
\]

Karena digunakan `sublinear_tf=True`, nilai frekuensi ditransformasikan menjadi:

\[
TF_{sublinear}(t,d) = 1 + \log(f(t,d))
\]

untuk \(f(t,d) > 0\).

### 4.2 Inverse Document Frequency

\[
IDF(t) = \log\left(\frac{1 + N}{1 + df(t)}\right) + 1
\]

dengan:

- \(N\) = jumlah dokumen pada data latih
- \(df(t)\) = jumlah dokumen yang memuat term \(t\)

### 4.3 Bobot akhir TF-IDF

\[
w_{t,d} = TF_{sublinear}(t,d) \times IDF(t)
\]

Setelah itu vektor dinormalisasi dengan norma L2:

\[
\hat{w}_{d} = \frac{w_d}{||w_d||_2}
\]

### 4.4 Contoh perhitungan sederhana

Misalkan kata "nyaman" muncul 2 kali dalam satu dokumen dan muncul pada 100 dokumen dari 1740 data latih.

\[
TF_{sublinear} = 1 + \log(2) = 1 + 0{,}6931 = 1{,}6931
\]

\[
IDF = \log\left(\frac{1+1740}{1+100}\right)+1
\]

\[
IDF = \log\left(\frac{1741}{101}\right)+1
      = \log(17{,}2376)+1
\]

\[
IDF \approx 2{,}8475 + 1 = 3{,}8475
\]

\[
TFIDF = 1{,}6931 \times 3{,}8475 \approx 6{,}5143
\]

Setelah itu nilai tersebut masih dinormalisasi bersama seluruh bobot term lain dalam dokumen yang sama.

## 5. Resampling pada Data Latih

Resampling hanya dilakukan pada data latih, bukan pada data uji.

### 5.1 Distribusi sebelum resample

\[
N_{latih,positif} = 1592
\]

\[
N_{latih,negatif} = 148
\]

Rasio ketidakseimbangan awal:

\[
Rasio = \frac{1592}{148} = 10{,}756757
\]

Artinya, kelas positif sekitar 10,76 kali lebih banyak daripada kelas negatif.

### 5.2 Jumlah tambahan data negatif

Karena kelas minoritas adalah negatif, maka dilakukan *oversampling*:

\[
Tambahan = 1592 - 148 = 1444
\]

### 5.3 Distribusi setelah resample

\[
N_{latih,positif}^{baru} = 1592
\]

\[
N_{latih,negatif}^{baru} = 1592
\]

\[
N_{latih}^{baru} = 1592 + 1592 = 3184
\]

Prior kelas setelah resample:

\[
P(Positif) = \frac{1592}{3184} = 0{,}5
\]

\[
P(Negatif) = \frac{1592}{3184} = 0{,}5
\]

Dengan demikian, data latih pada skenario *balance* menjadi simetris antar kelas.

## 6. Model Naive Bayes

Pada implementasi akhir, algoritma yang digunakan adalah `ComplementNB`, yaitu salah satu varian Naive Bayes yang lebih cocok untuk data tidak seimbang.

### 6.1 Rumus dasar Naive Bayes

Secara umum, Naive Bayes mengklasifikasikan dokumen \(d\) ke kelas \(c\) menggunakan:

\[
P(c|d) \propto P(c)\prod_{i=1}^{n} P(x_i|c)
\]

Dalam bentuk log:

\[
\log P(c|d) = \log P(c) + \sum_{i=1}^{n}\log P(x_i|c)
\]

### 6.2 Rumus Complement Naive Bayes

Untuk `ComplementNB`, estimasi probabilitas term dilakukan berdasarkan komplemen kelas:

\[
\hat{\theta}_{ci} = \frac{\alpha + \sum_{j:y_j \neq c} d_{ij}}
{\alpha |V| + \sum_{j:y_j \neq c}\sum_k d_{kj}}
\]

dengan:

- \(\alpha\) = parameter *smoothing*
- \(|V|\) = ukuran kosakata
- \(d_{ij}\) = bobot fitur ke-\(i\) pada dokumen ke-\(j\)

Skor kelas dihitung menggunakan bobot log dari komplemen kelas, lalu kelas dengan skor terbaik dipilih sebagai hasil prediksi.

### 6.3 Parameter yang diuji

Grid pencarian parameter:

\[
\alpha \in \{0{,}01,\ 0{,}05,\ 0{,}1,\ 0{,}5,\ 1{,}0,\ 10,\ 1000\}
\]

Skema validasi:

- `GridSearchCV`
- `cv=5`
- `scoring='f1_macro'`

### 6.4 Parameter terbaik

#### Skenario non-balance

\[
\alpha_{terbaik} = 1{,}0
\]

#### Skenario balance

\[
\alpha_{terbaik} = 0{,}01
\]

## 7. Model Support Vector Machine

Model yang digunakan adalah `LinearSVC`.

### 7.1 Fungsi keputusan

\[
f(x) = w \cdot x + b
\]

dengan:

- \(w\) = vektor bobot
- \(x\) = vektor TF-IDF
- \(b\) = bias

Aturan keputusan:

\[
f(x) > 0 \Rightarrow kelas\ positif
\]

\[
f(x) < 0 \Rightarrow kelas\ negatif
\]

### 7.2 Fungsi objektif SVM

Linear SVM meminimalkan:

\[
\min \frac{1}{2}||w||^2 + C\sum_{i=1}^{n}\xi_i
\]

dengan kendala:

\[
y_i(w \cdot x_i + b) \geq 1 - \xi_i,\quad \xi_i \geq 0
\]

### 7.3 Hinge loss

Untuk evaluasi margin:

\[
Hinge\ Loss = \frac{1}{N}\sum_{i=1}^{N}\max(0,\ 1-y_i f(x_i))
\]

dengan label kelas biasanya dikonversi ke \(\{-1,+1\}\).

### 7.4 Parameter dasar model

- `class_weight='balanced'`
- `max_iter=15000`
- `random_state=42`
- `dual=False`

### 7.5 Parameter yang diuji

\[
C \in \{0{,}01,\ 0{,}05,\ 0{,}1,\ 0{,}5,\ 1,\ 2\}
\]

Skema validasi:

- `GridSearchCV`
- `cv=5`
- `scoring='f1_macro'`

### 7.6 Parameter terbaik

#### Skenario non-balance

\[
C_{terbaik} = 0{,}05
\]

#### Skenario balance

\[
C_{terbaik} = 2
\]

## 8. Confusion Matrix Tiap Skenario

Pada bagian ini, kelas negatif diperlakukan sebagai baris pertama dan kelas positif sebagai baris kedua. Format confusion matrix:

\[
\begin{bmatrix}
TN_{negatif} & FP_{negatif} \\
FN_{positif} & TP_{positif}
\end{bmatrix}
\]

atau lebih tepat dibaca sebagai:

\[
\begin{bmatrix}
Actual\ Negatif \to Pred\ Negatif & Actual\ Negatif \to Pred\ Positif \\
Actual\ Positif \to Pred\ Negatif & Actual\ Positif \to Pred\ Positif
\end{bmatrix}
\]

### 8.1 Naive Bayes non-balance

Dari classification report:

- Negatif: precision 0,80, recall 0,54, support 37
- Positif: precision 0,96, recall 0,99, support 398

Confusion matrix yang konsisten dengan metrik tersebut adalah:

\[
CM_{NB,nonbalance}=
\begin{bmatrix}
20 & 17 \\
5 & 393
\end{bmatrix}
\]

Pemeriksaan:

\[
Recall_{negatif} = \frac{20}{20+17} = \frac{20}{37} = 0{,}5405
\]

\[
Recall_{positif} = \frac{393}{393+5} = \frac{393}{398} = 0{,}9874
\]

\[
Accuracy = \frac{20+393}{435} = \frac{413}{435} = 0{,}9494
\]

### 8.2 SVM non-balance

Classification report:

- Negatif: precision 0,62, recall 0,84, support 37
- Positif: precision 0,98, recall 0,95, support 398

Confusion matrix:

\[
CM_{SVM,nonbalance}=
\begin{bmatrix}
31 & 6 \\
19 & 379
\end{bmatrix}
\]

Pemeriksaan:

\[
Recall_{negatif} = \frac{31}{37} = 0{,}8378
\]

\[
Recall_{positif} = \frac{379}{398} = 0{,}9523
\]

\[
Accuracy = \frac{31+379}{435} = \frac{410}{435} = 0{,}9425
\]

### 8.3 Naive Bayes balance

Classification report:

- Negatif: precision 0,63, recall 0,73, support 37
- Positif: precision 0,97, recall 0,96, support 398

Confusion matrix:

\[
CM_{NB,balance}=
\begin{bmatrix}
27 & 10 \\
16 & 382
\end{bmatrix}
\]

Pemeriksaan:

\[
Recall_{negatif} = \frac{27}{37} = 0{,}7297
\]

\[
Recall_{positif} = \frac{382}{398} = 0{,}9598
\]

\[
Accuracy = \frac{27+382}{435} = \frac{409}{435} = 0{,}9402
\]

### 8.4 SVM balance

Classification report:

- Negatif: precision 0,77, recall 0,65, support 37
- Positif: precision 0,97, recall 0,98, support 398

Confusion matrix:

\[
CM_{SVM,balance}=
\begin{bmatrix}
24 & 13 \\
7 & 391
\end{bmatrix}
\]

Pemeriksaan:

\[
Recall_{negatif} = \frac{24}{37} = 0{,}6486
\]

\[
Recall_{positif} = \frac{391}{398} = 0{,}9824
\]

\[
Accuracy = \frac{24+391}{435} = \frac{415}{435} = 0{,}9540
\]

## 9. Rumus Evaluasi

### 9.1 Accuracy

\[
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
\]

### 9.2 Precision kelas tertentu

\[
Precision = \frac{TP}{TP + FP}
\]

### 9.3 Recall kelas tertentu

\[
Recall = \frac{TP}{TP + FN}
\]

### 9.4 F1-score kelas tertentu

\[
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
\]

### 9.5 Macro average

\[
F1_{macro} = \frac{F1_{negatif} + F1_{positif}}{2}
\]

### 9.6 Weighted average

Untuk metrik berbobot:

\[
Metric_{weighted} =
\frac{(support_{negatif} \times Metric_{negatif}) + (support_{positif} \times Metric_{positif})}
{support_{negatif} + support_{positif}}
\]

Pada data uji:

\[
support_{negatif} = 37,\quad support_{positif} = 398
\]

### 9.7 Balanced accuracy

\[
Balanced\ Accuracy = \frac{Recall_{negatif} + Recall_{positif}}{2}
\]

### 9.8 Log loss

Untuk Naive Bayes:

\[
LogLoss = -\frac{1}{N}\sum_{i=1}^{N}\sum_{c \in C} y_{ic}\log(p_{ic})
\]

### 9.9 Hinge loss

Untuk SVM:

\[
HingeLoss = \frac{1}{N}\sum_{i=1}^{N}\max(0,\ 1-y_i f(x_i))
\]

## 10. Hasil Numerik Akhir Tiap Model

### 10.1 Skenario non-balance

#### Naive Bayes

- alpha = 1,0
- accuracy = 0,9494252873563218
- precision weighted = 0,9450518643117466
- recall weighted = 0,9494252873563218
- f1 weighted = 0,9449065151231475
- f1 macro = 0,8089667837751517
- balanced accuracy = 0,7639888632350944
- log loss = 0,1615192496150586

#### SVM

- C = 0,05
- accuracy = 0,9425287356321839
- precision weighted = 0,9534193163158681
- recall weighted = 0,9425287356321839
- f1 weighted = 0,9463454734956915
- f1 macro = 0,8403575989782887
- balanced accuracy = 0,8950495721852505
- hinge loss = 0,4734711522457622

### 10.2 Skenario balance

#### Naive Bayes

- alpha = 0,01
- accuracy = 0,9402298850574713
- precision weighted = 0,945010337735736
- recall weighted = 0,9402298850574713
- f1 weighted = 0,9422442892477813
- f1 macro = 0,8210443037974684
- balanced accuracy = 0,844764362352302
- log loss = 0,17690452134513243

#### SVM

- C = 2
- accuracy = 0,9540229885057471
- precision weighted = 0,9513522542465592
- recall weighted = 0,9540229885057471
- f1 weighted = 0,9521665747733439
- f1 macro = 0,8404723485404137
- balanced accuracy = 0,815530354475078
- hinge loss = 0,1564654102573066

## 10A. Tabel Ringkas Hasil Pengujian

### 10A.1 Tabel hasil skenario non-balance

| Model | Parameter Terbaik | Accuracy | Precision Weighted | Recall Weighted | F1 Weighted | F1 Macro | Balanced Accuracy | Loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Naive Bayes | alpha = 1,0 | 0,9494 | 0,9451 | 0,9494 | 0,9449 | 0,8090 | 0,7640 | log loss = 0,1615 |
| SVM | C = 0,05 | 0,9425 | 0,9534 | 0,9425 | 0,9463 | 0,8404 | 0,8950 | hinge loss = 0,4735 |

### 10A.2 Tabel hasil skenario balance

| Model | Parameter Terbaik | Accuracy | Precision Weighted | Recall Weighted | F1 Weighted | F1 Macro | Balanced Accuracy | Loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Naive Bayes | alpha = 0,01 | 0,9402 | 0,9450 | 0,9402 | 0,9422 | 0,8210 | 0,8448 | log loss = 0,1769 |
| SVM | C = 2 | 0,9540 | 0,9514 | 0,9540 | 0,9522 | 0,8405 | 0,8155 | hinge loss = 0,1565 |

### 10A.3 Tabel perubahan balance terhadap non-balance

| Model | Delta Accuracy | Delta F1 Macro | Delta Balanced Accuracy | Delta Loss |
|---|---:|---:|---:|---:|
| Naive Bayes | -0,0092 | +0,0121 | +0,0808 | +0,0154 log loss |
| SVM | +0,0115 | +0,0001 | -0,0795 | -0,3170 hinge loss |

## 11. Selisih Hasil Balance dan Non-Balance

### 11.1 Naive Bayes

\[
\Delta Accuracy = 0{,}9402298850574713 - 0{,}9494252873563218 = -0{,}009195402298850519
\]

\[
\Delta F1_{macro} = 0{,}8210443037974684 - 0{,}8089667837751517 = 0{,}012077520022316657
\]

\[
\Delta BalancedAccuracy = 0{,}844764362352302 - 0{,}7639888632350944 = 0{,}0807754991172076
\]

\[
\Delta LogLoss = 0{,}17690452134513243 - 0{,}1615192496150586 = 0{,}01538527173007384
\]

Interpretasi:

- accuracy turun,
- tetapi F1 macro naik,
- balanced accuracy naik cukup besar,
- artinya model lebih baik mengenali kelas minoritas setelah resample.

### 11.2 SVM

\[
\Delta Accuracy = 0{,}9540229885057471 - 0{,}9425287356321839 = 0{,}011494252873563204
\]

\[
\Delta F1_{macro} = 0{,}8404723485404137 - 0{,}8403575989782887 = 0{,}0001147495621250938
\]

\[
\Delta BalancedAccuracy = 0{,}815530354475078 - 0{,}8950495721852505 = -0{,}07951921771017245
\]

\[
\Delta HingeLoss = 0{,}1564654102573066 - 0{,}4734711522457622 = -0{,}3170057419884556
\]

Interpretasi:

- accuracy naik,
- F1 macro hampir tetap,
- balanced accuracy turun,
- hinge loss turun,
- artinya resample meningkatkan performa agregat, tetapi tidak membuat kemampuan antar kelas menjadi lebih seimbang dibanding skenario non-balance.

## 12. Kesimpulan Matematis

Dari seluruh perhitungan di atas dapat disimpulkan:

1. Dataset akhir yang dipakai pemodelan berjumlah 2.175 data dari 2.449 data mentah.
2. Distribusi kelas awal sangat tidak seimbang: 91,4943% positif dan 8,5057% negatif.
3. Data dibagi menjadi 1.740 data latih dan 435 data uji dengan stratifikasi kelas.
4. TF-IDF dibentuk dengan konfigurasi unigram sampai trigram dan menghasilkan 5.123 fitur.
5. Resampling mengubah distribusi data latih dari 1592:148 menjadi 1592:1592.
6. Naive Bayes terbaik pada skenario non-balance memakai \(\alpha = 1{,}0\), sedangkan pada balance memakai \(\alpha = 0{,}01\).
7. SVM terbaik pada skenario non-balance memakai \(C = 0{,}05\), sedangkan pada balance memakai \(C = 2\).
8. SVM balance memberikan accuracy tertinggi sebesar 0,9540229885057471.
9. SVM non-balance memberikan balanced accuracy tertinggi sebesar 0,8950495721852505.
10. Secara matematis, resampling membantu Naive Bayes membaca kelas minoritas dengan lebih baik, sedangkan pada SVM resampling lebih meningkatkan performa agregat dibanding keseimbangan performa antar kelas.

## 13. Narasi Formal untuk Lampiran atau Sidang

Berdasarkan perhitungan matematis yang telah dilakukan, proses analisis sentimen pada penelitian ini menggunakan dua skenario eksperimen, yaitu skenario data latih asli yang tidak seimbang dan skenario data latih yang telah diseimbangkan melalui *resampling* pada kelas minoritas. Dataset akhir yang digunakan pada tahap pemodelan berjumlah 2.175 data, dengan distribusi 1.990 data sentimen positif dan 185 data sentimen negatif. Data tersebut kemudian dibagi menjadi 1.740 data latih dan 435 data uji menggunakan metode *stratified train-test split* dengan rasio 80:20 agar proporsi kelas tetap terjaga pada kedua subset.

Representasi dokumen dilakukan menggunakan metode TF-IDF dengan konfigurasi *ngram* 1 sampai 3, `max_df = 0.9`, `min_df = 2`, `sublinear_tf = True`, dan normalisasi `l2`, sehingga diperoleh 5.123 fitur. Pada skenario non-balance, model Naive Bayes terbaik diperoleh pada parameter \(\alpha = 1{,}0\), sedangkan model SVM terbaik diperoleh pada parameter \(C = 0{,}05\). Pada skenario balance, model Naive Bayes terbaik diperoleh pada \(\alpha = 0{,}01\), sedangkan model SVM terbaik diperoleh pada \(C = 2\).

Hasil perhitungan menunjukkan bahwa pada skenario non-balance, Naive Bayes memperoleh *accuracy* sebesar 0,9494, sedangkan SVM memperoleh *accuracy* sebesar 0,9425. Namun, SVM pada skenario ini memberikan *balanced accuracy* tertinggi, yaitu 0,8950, yang menunjukkan kemampuan lebih baik dalam menjaga keseimbangan pengenalan antar kelas. Pada skenario balance, Naive Bayes memperoleh *accuracy* sebesar 0,9402 dan SVM memperoleh *accuracy* tertinggi sebesar 0,9540. Di sisi lain, *balanced accuracy* SVM pada skenario balance turun menjadi 0,8155.

Dengan demikian, secara matematis dapat disimpulkan bahwa proses *resampling* memberikan dampak yang berbeda pada masing-masing algoritma. Pada Naive Bayes, *resampling* menurunkan *accuracy* tetapi meningkatkan *F1 macro* dan *balanced accuracy*, sehingga model menjadi lebih sensitif terhadap kelas minoritas. Pada SVM, *resampling* meningkatkan *accuracy* dan *F1 weighted*, tetapi menurunkan *balanced accuracy*. Oleh sebab itu, apabila penilaian didasarkan pada performa agregat secara keseluruhan, maka SVM pada skenario balance merupakan model terbaik. Akan tetapi, apabila fokus diarahkan pada keseimbangan deteksi antar kelas, maka SVM pada skenario non-balance memberikan hasil yang paling kuat.

## 14. Contoh Perhitungan Manual Satu Ulasan

Bagian ini diberikan sebagai ilustrasi alur hitung manual. Nilai pada contoh ini bertujuan menunjukkan mekanisme perhitungan dan bukan menggantikan hasil prediksi aktual model yang dihitung otomatis oleh sistem.

### 14.1 Contoh ulasan

Misalkan terdapat satu ulasan:

> "hotel nyaman lokasi strategis pelayanan ramah"

Setelah preprocessing, token misalnya menjadi:

\[
[\text{hotel},\ \text{nyaman},\ \text{lokasi},\ \text{strategis},\ \text{layan},\ \text{ramah}]
\]

Jumlah token:

\[
|d| = 6
\]

### 14.2 Contoh pembobotan TF-IDF

Misalkan dari data latih diketahui frekuensi dokumen untuk tiap kata sebagai berikut:

| Term | \(df(t)\) |
|---|---:|
| hotel | 1200 |
| nyaman | 250 |
| lokasi | 400 |
| strategis | 180 |
| layan | 350 |
| ramah | 220 |

Jumlah dokumen latih:

\[
N = 1740
\]

Karena tiap kata muncul satu kali pada dokumen contoh, maka dengan `sublinear_tf=True`:

\[
TF_{sublinear} = 1 + \log(1) = 1
\]

#### a. Kata `hotel`

\[
IDF(\text{hotel}) = \log\left(\frac{1741}{1201}\right) + 1
\]

\[
IDF(\text{hotel}) \approx \log(1{,}4496) + 1
\]

\[
IDF(\text{hotel}) \approx 0{,}3713 + 1 = 1{,}3713
\]

\[
TFIDF(\text{hotel}) = 1 \times 1{,}3713 = 1{,}3713
\]

#### b. Kata `nyaman`

\[
IDF(\text{nyaman}) = \log\left(\frac{1741}{251}\right) + 1
\]

\[
IDF(\text{nyaman}) \approx \log(6{,}9363) + 1
\]

\[
IDF(\text{nyaman}) \approx 1{,}9368 + 1 = 2{,}9368
\]

\[
TFIDF(\text{nyaman}) = 1 \times 2{,}9368 = 2{,}9368
\]

#### c. Kata `lokasi`

\[
IDF(\text{lokasi}) = \log\left(\frac{1741}{401}\right) + 1
\]

\[
IDF(\text{lokasi}) \approx \log(4{,}3416) + 1
\]

\[
IDF(\text{lokasi}) \approx 1{,}4682 + 1 = 2{,}4682
\]

\[
TFIDF(\text{lokasi}) = 1 \times 2{,}4682 = 2{,}4682
\]

#### d. Kata `strategis`

\[
IDF(\text{strategis}) = \log\left(\frac{1741}{181}\right) + 1
\]

\[
IDF(\text{strategis}) \approx \log(9{,}6188) + 1
\]

\[
IDF(\text{strategis}) \approx 2{,}2637 + 1 = 3{,}2637
\]

\[
TFIDF(\text{strategis}) = 1 \times 3{,}2637 = 3{,}2637
\]

#### e. Kata `layan`

\[
IDF(\text{layan}) = \log\left(\frac{1741}{351}\right) + 1
\]

\[
IDF(\text{layan}) \approx \log(4{,}9601) + 1
\]

\[
IDF(\text{layan}) \approx 1{,}6014 + 1 = 2{,}6014
\]

\[
TFIDF(\text{layan}) = 1 \times 2{,}6014 = 2{,}6014
\]

#### f. Kata `ramah`

\[
IDF(\text{ramah}) = \log\left(\frac{1741}{221}\right) + 1
\]

\[
IDF(\text{ramah}) \approx \log(7{,}8778) + 1
\]

\[
IDF(\text{ramah}) \approx 2{,}0640 + 1 = 3{,}0640
\]

\[
TFIDF(\text{ramah}) = 1 \times 3{,}0640 = 3{,}0640
\]

Maka vektor bobot sebelum normalisasi:

\[
[1{,}3713,\ 2{,}9368,\ 2{,}4682,\ 3{,}2637,\ 2{,}6014,\ 3{,}0640]
\]

### 14.3 Contoh keputusan dengan Naive Bayes

Misalkan dari model hasil pelatihan diperoleh:

\[
P(Positif)=0{,}914943
,\quad
P(Negatif)=0{,}085057
\]

Misalkan bobot probabilitas term yang telah dipelajari model adalah:

| Term | \(P(t|Positif)\) | \(P(t|Negatif)\) |
|---|---:|---:|
| hotel | 0,060 | 0,040 |
| nyaman | 0,050 | 0,010 |
| lokasi | 0,040 | 0,015 |
| strategis | 0,030 | 0,008 |
| layan | 0,045 | 0,020 |
| ramah | 0,035 | 0,010 |

Maka:

\[
Score(Positif) \propto P(Positif)\times
0{,}060\times0{,}050\times0{,}040\times0{,}030\times0{,}045\times0{,}035
\]

\[
Score(Positif) \propto 0{,}914943 \times 5{,}67 \times 10^{-10}
\]

\[
Score(Positif) \propto 5{,}1886 \times 10^{-10}
\]

Sedangkan:

\[
Score(Negatif) \propto P(Negatif)\times
0{,}040\times0{,}010\times0{,}015\times0{,}008\times0{,}020\times0{,}010
\]

\[
Score(Negatif) \propto 0{,}085057 \times 9{,}6 \times 10^{-13}
\]

\[
Score(Negatif) \propto 8{,}1655 \times 10^{-14}
\]

Karena:

\[
Score(Positif) > Score(Negatif)
\]

maka dokumen diprediksi sebagai:

\[
\text{Positif}
\]

### 14.4 Contoh keputusan dengan SVM

Misalkan model SVM menghasilkan bobot sederhana berikut untuk enam fitur tadi:

| Term | Bobot \(w_i\) |
|---|---:|
| hotel | 0,10 |
| nyaman | 0,80 |
| lokasi | 0,45 |
| strategis | 0,70 |
| layan | 0,60 |
| ramah | 0,75 |

Misalkan bias:

\[
b = -1{,}20
\]

Dengan vektor TF-IDF contoh:

\[
x = [1{,}3713,\ 2{,}9368,\ 2{,}4682,\ 3{,}2637,\ 2{,}6014,\ 3{,}0640]
\]

Maka fungsi keputusan:

\[
f(x)=w\cdot x+b
\]

\[
f(x)=
(0{,}10)(1{,}3713)+
(0{,}80)(2{,}9368)+
(0{,}45)(2{,}4682)+
(0{,}70)(3{,}2637)+
(0{,}60)(2{,}6014)+
(0{,}75)(3{,}0640)-1{,}20
\]

\[
f(x)=
0{,}1371+
2{,}3494+
1{,}1107+
2{,}2846+
1{,}5608+
2{,}2980-
1{,}20
\]

\[
f(x)=8{,}5406
\]

Karena:

\[
f(x) > 0
\]

maka dokumen diprediksi sebagai:

\[
\text{Positif}
\]

### 14.5 Makna contoh manual

Contoh di atas menunjukkan bahwa satu ulasan melewati tahapan:

1. preprocessing teks,
2. konversi ke fitur TF-IDF,
3. perhitungan skor kelas pada Naive Bayes,
4. perhitungan fungsi keputusan pada SVM,
5. penetapan label akhir.

Pada implementasi nyata proyek, seluruh proses tersebut dilakukan otomatis oleh model hasil pelatihan pada ribuan fitur dan bukan hanya pada beberapa kata contoh seperti ilustrasi di atas.

## 15. Penutup Lampiran

Dokumen perhitungan ini menunjukkan bahwa seluruh proses analisis sentimen pada proyek TA telah dibangun di atas tahapan matematis yang jelas, mulai dari representasi data, penyeimbangan kelas, pembentukan model, hingga evaluasi performa. Dengan adanya dua skenario pengujian, yaitu data asli dan data hasil *resample*, penelitian ini tidak hanya mengejar nilai akurasi tertinggi, tetapi juga memperhatikan kemampuan model dalam mengenali kelas minoritas.

Secara keseluruhan, SVM pada skenario data latih seimbang memberikan performa agregat terbaik, sedangkan SVM pada skenario data latih tidak seimbang memberikan nilai *balanced accuracy* tertinggi. Oleh karena itu, hasil penelitian ini dapat dipertanggungjawabkan baik secara implementatif maupun secara matematis sebagai dasar pemilihan model terbaik pada sistem monitoring sentimen ulasan hotel.
