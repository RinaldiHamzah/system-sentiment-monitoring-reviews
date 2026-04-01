# Analisis Sentimen Ulasan Hotel

Repository ini berisi pipeline analisis data dan pelatihan model machine learning untuk klasifikasi sentimen ulasan hotel (POSITIF/NEGATIF).

## 1. Tujuan

- Melakukan preprocessing teks ulasan berbahasa Indonesia.
- Melakukan pelabelan data ulasan.
- Melatih dan mengevaluasi model klasifikasi sentimen.
- Menyimpan artefak model (`.pkl`) untuk dipakai di aplikasi utama.

## 2. Ruang Lingkup

- Dataset ulasan hotel dari Google Maps.
- Tahapan pemrosesan teks: normalisasi, stopword filtering, stemming.
- Ekstraksi fitur menggunakan TF-IDF.
- Pelatihan model:
  - Multinomial Naive Bayes
  - Support Vector Machine (Linear SVM)
- Perbandingan dua skenario:
  - Tanpa SMOTE (normal)
  - Dengan SMOTE

## 3. Struktur Folder

```text
analisis/
|- analisis.ipynb
|- analisis_smote.ipynb
|- labeling.ipynb
|- ekstraksi.py
|- test.py
|- README.md
|- data/
|  |- raw/
|  |  |- data_aveta.csv
|  |  |- normalisasi_aveta.csv
|  |  |- stopword_aveta.csv
|  |- prosses/
|     |- hasil_preprosesing_aveta_tr.csv
|     |- hasil_labeling_aveta_transformer_tr.csv
|     |- stemming.csv
|     |- final_aveta_tr.csv
|- model_machine/
|  |- naive_bayes_model.pkl
|  |- SVM_model.pkl
|  |- vectorizer.pkl
|  |- metrics_nb_svm.json
|- model_machine_smote/
   |- naive_bayes_model_smote.pkl
   |- SVM_model_smote.pkl
   |- vectorizer_smote.pkl
   |- metrics_nb_svm_smote.json
```

## 4. Kebutuhan Lingkungan

- Python 3.10+
- pip
- Jupyter Notebook (opsional)

Install dependency minimum:

```bash
python -m venv env
env\Scripts\activate
pip install pandas numpy scikit-learn imbalanced-learn joblib jupyter
```

## 5. Alur Eksperimen

1. Siapkan data mentah pada `data/raw/data_aveta.csv`.
2. Jalankan preprocessing dan labeling pada notebook/script.
3. Simpan data olahan ke `data/prosses/`.
4. Latih model:
   - `analisis.ipynb` untuk skenario normal.
   - `analisis_smote.ipynb` untuk skenario SMOTE.
5. Simpan model + metrik ke folder model masing-masing.

## 6. Hasil Evaluasi Model

Sumber metrik:
- `model_machine/metrics_nb_svm.json`
- `model_machine_smote/metrics_nb_svm_smote.json`

### 6.1 Skenario Normal (tanpa SMOTE)

- TF-IDF vocabulary size: **5123**

| Model | Accuracy | F1 Weighted | F1 Macro | Balanced Accuracy |
|---|---:|---:|---:|---:|
| Naive Bayes (alpha=0.05) | 0.9172 | 0.9276 | 0.8034 | 0.9180 |
| SVM (C=1) | **0.9609** | **0.9607** | **0.8729** | 0.8683 |

### 6.2 Skenario SMOTE

- TF-IDF vocabulary size: **5123**

| Model | Accuracy | F1 Weighted | F1 Macro | Balanced Accuracy |
|---|---:|---:|---:|---:|
| Naive Bayes (alpha=0.01) | 0.9379 | 0.9403 | 0.8162 | **0.8435** |
| SVM (C=2) | **0.9540** | **0.9522** | **0.8405** | 0.8155 |

### 6.3 Ringkasan Perbandingan

- **Akurasi tertinggi keseluruhan**: SVM tanpa SMOTE (**0.9609**).
- **F1 Macro tertinggi**: SVM tanpa SMOTE (**0.8729**).
- Pada eksperimen ini, SMOTE tidak meningkatkan performa SVM utama terhadap skenario normal.
- Naive Bayes mengalami kenaikan akurasi saat SMOTE (0.9172 -> 0.9379), tetapi tetap di bawah SVM.

## 7. Rekomendasi Model Produksi

Berdasarkan metrik saat ini, model yang direkomendasikan untuk deployment adalah:

- **SVM tanpa SMOTE** (folder `model_machine/`):
  - `SVM_model.pkl`
  - `vectorizer.pkl`

Alasan:
- Memberikan akurasi dan F1 terbaik pada data evaluasi.
- Stabil untuk klasifikasi sentimen biner pada dataset saat ini.

## 8. Menjalankan Notebook

```bash
jupyter notebook
```

Notebook utama:
- `labeling.ipynb`
- `analisis.ipynb`
- `analisis_smote.ipynb`


## 9. Catatan Penting

- Nama folder `data/prosses` dipertahankan mengikuti struktur proyek yang sudah ada.
- Jaga konsistensi versi `scikit-learn` antara training dan inferensi untuk menghindari warning kompatibilitas pickle.
- Jangan simpan credential/API key pada repository ini.

## 10. Pengembangan Lanjutan (Opsional)

- Tambahkan evaluasi per kelas (precision/recall per label).
- Tambahkan validasi silang (cross-validation) untuk hasil lebih robust.
- Bandingkan dengan model lain (Logistic Regression, Random Forest, IndoBERT, dll).
