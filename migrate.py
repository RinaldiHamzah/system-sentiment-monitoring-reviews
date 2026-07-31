import mysql.connector
import psycopg2
import pandas as pd
import urllib.parse

# ==========================================
# 1. KONFIGURASI DATABASE
# ==========================================

# Database Asal (MySQL)
MYSQL_CONFIG = {
    'host': 'localhost',                        
    'user': 'root',            
    'password': '',            
    'database': 'monitoring_review' 
}

# Database Tujuan (Supabase PostgreSQL)
password_aman = urllib.parse.quote_plus("Rinaldi001445##RH")
SUPABASE_URI = f"postgresql://postgres:{password_aman}@db.inbgjbeofhvuzotirfru.supabase.co:5432/postgres"

# Daftar semua tabel yang ingin dimigrasi secara berurutan
DAFTAR_TABEL = [
    "hotels",
    "users",
    "hotel_reviews",
    "sentiment_reviews",
    "telegram_users",
    "notifications"]

# ==========================================
# 2. PROSES MIGRASI DATA MULTI-TABEL
# ==========================================
def jalankan_migrasi():
    try:
        # 1. Hubungkan ke Database Asal & Tujuan
        print("🔌 Menyambungkan ke database MySQL dan Supabase...")
        conn_mysql = mysql.connector.connect(**MYSQL_CONFIG)
        conn_supabase = psycopg2.connect(SUPABASE_URI)
        cursor_supabase = conn_supabase.cursor()
        
        print("Koneksi berhasil! Memulai proses migrasi...\n")

        # 2. Perulangan untuk memproses setiap tabel
        for tabel in DAFTAR_TABEL:
            print(f"🔄 Migrating tabel: {tabel}")
            
            # Ambil data dari MySQL
            query_select = f"SELECT * FROM {tabel}"
            
            # Menggunakan conn_mysql.cursor().connection untuk meredam UserWarning dari Pandas
            df = pd.read_sql(query_select, conn_mysql)
            print(f"   📊 {len(df)} rows ditemukan di MySQL")
            
            # Jika tabel kosong, lanjut ke tabel berikutnya
            if df.empty:
                print(f"   ⚠️ Tabel {tabel} kosong, dilewati.")
                print(f"   ✓ {tabel} selesai\n")
                continue

            # -------------------------------------------------------------
            # PERBAIKAN: Konversi angka 1/0 atau int ke Boolean untuk Supabase
            # Jika ada kolom dengan nama 'is_active' atau kolom boolean lainnya, 
            # kita paksa tipenya menjadi boolean asli Python (True/False)
            # -------------------------------------------------------------
            for col in df.columns:
                # Otomatis mendeteksi kolom berawalan 'is_' (seperti is_active) atau bertipe int yang berisi 0/1
                if col.startswith('is_') or df[col].dtype == 'int64':
                    # Cek jika isi kolomnya hanya variasi dari 0, 1, atau None/NaN
                    if df[col].isin([0, 1, None, float('nan')]).all():
                        df[col] = df[col].astype(bool)
                        # Kembalikan yang NaN/None menjadi None agar tidak berubah jadi True
                        df[col] = df[col].where(df[col].notna(), None)
            # -------------------------------------------------------------

            # Buat query INSERT dinamis sesuai kolom tabel
            kolom = ",".join([f'"{c}"' for c in df.columns]) # Ditambah tanda petik dua ganda agar aman dari reserved keyword Postgres
            placeholders = ",".join(["%s"] * len(df.columns))
            query_insert = f"INSERT INTO {tabel} ({kolom}) VALUES ({placeholders})"
            
            # Masukkan data ke Supabase baris demi baris
            # Kita bersihkan data NaN/NaT agar dikenali sebagai NULL di PostgreSQL
            df_clean = df.astype(object).where(pd.notnull(df), None)
            
            for row in df_clean.itertuples(index=False):
                cursor_supabase.execute(query_insert, tuple(row))
            
            # Commit setiap kali satu tabel selesai agar data tersimpan
            conn_supabase.commit()
            print(f"   ✓ {tabel} selesai bermigrasi\n")

        # 3. Tutup semua koneksi jika semua tabel selesai
        cursor_supabase.close()
        conn_supabase.close()
        conn_mysql.close()
        
        print("🎉 ISI SEMUA TABEL BERHASIL DIMIGRASIKAN DENGAN SUKSES!")

    except Exception as e:
        # Jika terjadi error, batalkan transaksi yang menggantung agar tidak mengunci database
        if 'conn_supabase' in locals():
            conn_supabase.rollback()
        print(f"Terjadi kesalahan saat migrasi: {e}")

if __name__ == "__main__":
    jalankan_migrasi()