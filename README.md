System Sentiment Monitoring Reviews

##  About

Sistem monitoring sentimen real-time untuk ulasan Google Maps menggunakan **TF-IDF feature engineering**, **Naive Bayes**, dan **Support Vector Machine (SVM)** yang di-deploy menggunakan Flask.

Proyek ini merepresentasikan implementasi lengkap workflow Machine Learning mulai dari preprocessing data, pelatihan model, evaluasi, hingga deployment berbasis web.

---

# Latar Belakang Masalah

Ulasan pengguna pada Google Maps mengandung informasi penting mengenai kepuasan pelanggan. Namun, data tersebut bersifat tidak terstruktur (unstructured text).

Sistem ini dirancang untuk:

* Mengubah teks ulasan menjadi fitur numerik
* Mengklasifikasikan sentimen (positif/negatif)
* Menyajikan hasil dalam dashboard monitoring

---

# Arsitektur Sistem

```text
Client (Browser)
        ↓
Flask Backend
        ↓
Preprocessing Pipeline
        ↓
TF-IDF Vectorization
        ↓
Model Inference (NB / SVM)
        ↓
Hasil Prediksi
        ↓
Dashboard Analitik
```

---

#  Pipeline Machine Learning

## Data Preprocessing

* Case folding (lowercase)
* Tokenisasi
* Stopword removal
* Stemming
* Pembersihan simbol dan karakter tidak relevan

Pipeline dipisahkan dalam folder `pipeline/` untuk menjaga modularitas dan kemudahan maintenance.

## Feature Engineering

* TF-IDF Vectorizer
* Normalisasi L2
* Representasi sparse matrix

Vectorizer diserialisasi menggunakan `joblib` untuk memastikan konsistensi transformasi saat inference.


## Model Machine Learning

### Multinomial Naive Bayes

* Probabilistic classifier
* Cepat dan efisien untuk teks

### Support Vector Machine (Linear Kernel)

* Margin maximization
* Generalisasi lebih baik pada data berdimensi tinggi


# Evaluasi Model

Model dievaluasi menggunakan:

| Model       | Accuracy | F1-Score |
| ----------- | -------- | -------- |
| Naive Bayes | 89%      | 88%      |
| SVM         | 91%      | 91%      |


# Cara Menjalankan
## Clone Repository

```
git clone https://github.com/yourusername/system-sentiment-monitoring-reviews.git
cd system-sentiment-monitoring-reviews
```

# Pertimbangan Engineering

✔ Pemisahan training dan inference
✔ Model diserialisasi untuk production use
✔ Struktur modular dan scalable
✔ Reproducible environment via requirements.txt
✔ Siap dikembangkan menjadi REST API

---

# Teknologi yang Digunakan

* Python
* Flask
* Scikit-learn
* Pandas
* NumPy
* Joblib
* HTML/CSS/JavaScript


# Potensi Pengembangan

* Deployment ke cloud (AWS / GCP / Render)
* Konversi ke REST API (FastAPI)
* Docker containerization
* CI/CD pipeline
* Monitoring & logging sistem
* Integrasi MLflow untuk experiment tracking
* Integrasi model deep learning (LSTM / BERT)

Repository ini menunjukkan kemampuan:

* Implementasi end-to-end NLP pipeline
* Feature engineering (TF-IDF)
* Perbandingan dua algoritma klasifikasi
* Integrasi model ke dalam sistem web
* Struktur kode yang modular dan maintainable
* Kesiapan deployment produksi

