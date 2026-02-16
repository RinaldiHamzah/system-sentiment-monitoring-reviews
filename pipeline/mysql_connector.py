# mysql_connector.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from collections import Counter 
import re
   
#  KONFIGURASI DATABASE
db_config = {
    "host": "localhost",       # ganti kalau server MySQL di remote
    "user": "root",            # username MySQL
    "password": "",            # password MySQL
    "database": "smart_review" # nama database
}
def get_connection():
    return mysql.connector.connect(**db_config)

#  FUNGSI AKSES DATABASE

def save_user(username, password_hash, role="user"):
    """Simpan user baru ke tabel users"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, password_hash, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

def save_hotel_review(hotel_id, user_name, review_text, rating, review_date, source):
    """Simpan review mentah ke hotel_reviews"""
    conn = get_connection()
    cursor = conn.cursor()

    # Normalisasi review_date
    if isinstance(review_date, str):
        try:
            review_date = datetime.fromisoformat(review_date)
        except:
            review_date = datetime.now()
    elif isinstance(review_date, (int, float)):
        review_date = datetime.fromtimestamp(review_date)
    elif not isinstance(review_date, datetime):
        review_date = datetime.now()

    cursor.execute("""
        INSERT INTO hotel_reviews 
        (hotel_id, user_name, review_text, rating, review_date, source, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, (hotel_id, user_name, review_text, rating, review_date, source))

    review_id = cursor.lastrowid
    conn.commit()
    cursor.close(); conn.close()
    return review_id


def save_sentiment_review(review_id, sentiment_nb, sentiment_svm):
    """Simpan hasil analisis sentimen ke tabel sentiment_reviews"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data dari hotel_reviews
    cursor.execute("SELECT * FROM hotel_reviews WHERE review_id = %s", (review_id,))
    hr = cursor.fetchone()
    if not hr:
        cursor.close(); conn.close()
        raise ValueError(f"Tidak ada hotel_review dengan review_id={review_id}")

    review_date = hr["review_date"] or datetime.now()

    cursor.execute("""
        INSERT INTO sentiment_reviews 
        (review_id, hotel_id, user_name, review_text, rating, review_date, 
         sentiment_nb, sentiment_svm, source, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
    """, (
        hr["review_id"], hr["hotel_id"], hr["user_name"], hr["review_text"],
        hr["rating"], review_date, sentiment_nb, sentiment_svm, hr["source"]
    ))

    sid = cursor.lastrowid
    conn.commit()
    cursor.close(); conn.close()
    return sid

def get_all_users():
    """Ambil semua user dari tabel users"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_reviews_by_hotel(hotel_id):
    """Ambil semua review berdasarkan hotel_id"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hotel_reviews WHERE hotel_id = %s", (hotel_id,))
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return reviews

def save_telegram_user(chat_id):
    """Simpan user Telegram ke DB (subscribed=True)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telegram_users (chat_id, subscribed) VALUES (%s, TRUE) "
        "ON DUPLICATE KEY UPDATE subscribed=TRUE",
        (chat_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()

def log_notification(review_id, chat_id, status="sent"):
    """Log status pengiriman notifikasi ke tabel notifications"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (review_id, chat_id, status) VALUES (%s, %s, %s)",
        (review_id, chat_id, status)
    )
    conn.commit()
    cursor.close()
    conn.close()

# db:scraper.py
def is_new_review(review_text):
    """Cek apakah review sudah ada di DB"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM hotel_reviews WHERE review_text = %s", (review_text,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count == 0


def save_hotel_review_raw(hotel_id, review_text, review_date, rating, user_name, source="Google Maps"):
    """Simpan review mentah hasil scraping ke DB"""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO hotel_reviews (hotel_id, review_text, review_date, rating, user_name, source)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (hotel_id, review_text, review_date, rating, user_name, source))
    conn.commit()
    review_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return review_id

# notif_telegram.py
def send_telegram_alert(review_text, sentiment_nb, sentiment_svm, rating=None, user='System'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM telegram_users WHERE subscribed=TRUE")
    chat_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

# Users
def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return row

def create_user(username, password, role="user"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
                (username, password, role))
    conn.commit()
    cur.close(); conn.close()

# update password
def update_user_password(username, new_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_hash, username))
    conn.commit()
    conn.close()    

# Hotels
def get_hotel(hotel_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM hotels WHERE hotel_id=%s", (hotel_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return row

# hotel_reviews (raw)
def save_hotel_review(hotel_id, user_name, review_text, rating, review_date=None, source="Google Maps"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO hotel_reviews (hotel_id, user_name, review_text, rating, review_date, source)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (hotel_id, user_name, review_text, rating, review_date, source))
    conn.commit()
    rid = cur.lastrowid
    cur.close(); conn.close()
    return rid

# sentiment_reviews (ML results)/ sentiment storage
def save_sentiment_review(review_id, hotel_id, user_name, review_text, rating, review_date, nb, svm, source="Google Maps"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sentiment_reviews 
        (review_id, hotel_id, user_name, review_text, rating, review_date, sentiment_nb, sentiment_svm, source) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (review_id, hotel_id, user_name, review_text, rating, review_date, nb, svm, source))
    conn.commit()
    sid = cur.lastrowid
    cur.close(); conn.close()
    return sid


# uji coba cek duplikasi hasil review
def review_exists(hotel_id, user_name, text, rating, source):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if text is None:
        query = """
            SELECT review_id FROM hotel_reviews
            WHERE hotel_id = %s AND user_name = %s
              AND review_text IS NULL AND rating = %s AND source = %s
            LIMIT 1
        """
        params = (hotel_id, user_name, rating, source)
    else:
        query = """
            SELECT review_id FROM hotel_reviews
            WHERE hotel_id = %s AND user_name = %s
              AND review_text = %s AND rating = %s AND source = %s
            LIMIT 1
        """
        params = (hotel_id, user_name, text, rating, source)

    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None



# uji coba db menhitung selisish review
def get_review_stats(hotel_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Hitung total semua review
    cur.execute("SELECT COUNT(*) AS total FROM sentiment_reviews WHERE hotel_id=%s", (hotel_id,))
    total = cur.fetchone()["total"]

    # Hitung minggu ini
    cur.execute("""
        SELECT COUNT(*) AS c 
        FROM sentiment_reviews 
        WHERE hotel_id=%s AND review_date >= CURDATE() - INTERVAL 7 DAY
    """, (hotel_id,))
    this_week = cur.fetchone()["c"]

    # Hitung minggu lalu
    cur.execute("""
        SELECT COUNT(*) AS c 
        FROM sentiment_reviews 
        WHERE hotel_id=%s 
          AND review_date >= CURDATE() - INTERVAL 14 DAY
          AND review_date < CURDATE() - INTERVAL 7 DAY
    """, (hotel_id,))
    last_week = cur.fetchone()["c"]
    cur.close()
    conn.close()
    return total, this_week - last_week

# dasboard wely review
def get_weekly_comparison(hotel_id):
    """
    Hitung jumlah review minggu ini vs minggu lalu.
    Berdasarkan kolom review_date di hotel_reviews.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT 
      SUM(CASE WHEN YEARWEEK(review_date, 1) = YEARWEEK(CURDATE(), 1) THEN 1 ELSE 0 END) AS this_week,
      SUM(CASE WHEN YEARWEEK(review_date, 1) = YEARWEEK(CURDATE(), 1) - 1 THEN 1 ELSE 0 END) AS last_week
    FROM hotel_reviews
    WHERE hotel_id = %s;
    """
    cursor.execute(sql, (hotel_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "this_week": row["this_week"] or 0,
        "last_week": row["last_week"] or 0
    }

# Uji coba dasboard avg rating/rating distribution/latest review
def get_latest_reviews(hotel_id, limit=1):
    """
    Ambil review terbaru. Default hanya 1, tapi bisa lebih.
    Return list of dict.
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT user_name, review_text, rating, source, review_date,
               sentiment_nb, sentiment_svm
        FROM sentiment_reviews
        WHERE hotel_id = %s
        ORDER BY review_date DESC
        LIMIT %s
    """, (hotel_id, limit))
    rows = cur.fetchall()
    cur.close()
    return rows if rows else []

def get_rating_distribution(hotel_id):
    """
    Return distribusi rating (1-5) dalam bentuk dict.
    Contoh: {1: 2, 2: 5, 3: 10, 4: 20, 5: 50}
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT rating, COUNT(*) as count
        FROM hotel_reviews
        WHERE hotel_id = %s
        GROUP BY rating
    """, (hotel_id,))
    rows = cur.fetchall()
    cur.close()

    # Default semua rating 0
    dist = {i: 0 for i in range(1, 6)}
    for row in rows:
        dist[row["rating"]] = row["count"]

    return dist

def get_average_rating(hotel_id):
    """
    Return rata-rata rating (float, 2 decimal).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT AVG(rating) 
        FROM hotel_reviews
        WHERE hotel_id = %s
    """, (hotel_id,))
    avg = cur.fetchone()[0]
    cur.close()
    return round(avg, 2) if avg else 0.0

# Uji coba keywords analytics
def get_top_keywords(hotel_id, limit=10, lang="id"):
    """
    Ambil kata paling sering muncul di review berdasarkan sentimen.
    Bisa pilih stopwords sesuai bahasa (?lang=id atau en).
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT review_text, sentiment_nb FROM sentiment_reviews WHERE hotel_id=%s", (hotel_id,))
    rows = cur.fetchall()
    cur.close(); conn.close()

    # Stopwords sederhana (bisa diperluas)
    stopwords_id = {"dan","yang","di","ke","dari","itu","ini","ada","tidak","sangat","saya","juga",
                    'dan', 'yang', 'lalu', 'yg', 'saya', 'sy', 'lagi',
             'nya', 'untuk', 'utk', 'udah', 'sudah', 'udh', 'sdh', 'aja', 'tapi',
             'lagi', 'buat', 'ya', 'itu', 'kalo', 'klo','ga','ok', 'oke', 'OK'
             'ada', 'adalah', 'adanya', 'adapun', 'agak', 'agaknya', 'agar', 'akan',
             'akankah', 'akhir', 'akhiri', 'akhirnya', 'aku', 'akulah', 'amat', 'amatlah',
             'anda', 'andalah', 'antar', 'antara', 'antaranya', 'apa', 'apaan', 'apabila',
             'apakah', 'apalagi', 'apatah', 'artinya', 'asal', 'asalkan', 'atas', 'atau',
             'ataukah', 'ataupun', 'awal', 'awalnya', 'bagai', 'bagaikan', 'bagaimana',
             'bagaimanakah', 'bagaimanapun', 'bagi', 'bagian', 'bahkan', 'bahwa', 'bahwasanya',
             'baik', 'bakal', 'bakalan', 'balik', 'banyak', 'bapak', 'baru', 'bawah',
             'beberapa', 'begini', 'beginian', 'beginikah', 'beginilah', 'begitu', 'begitukah',
             'begitulah', 'begitupun', 'bekerja', 'belakang', 'belakangan', 'belum', 'belumlah',
             'benar', 'benarkah', 'benarlah', 'berada', 'berakhir', 'berakhirlah', 'berakhirnya',
             'berapa', 'berapakah', 'berapalah', 'berapapun', 'berarti', 'berawal', 'berbagai',
             'berdatangan', 'beri', 'berikan', 'berikut', 'berikutnya', 'berjumlah', 'berkali-kali',
             'berkata', 'berkehendak', 'berkeinginan', 'berkenaan', 'berlainan', 'berlalu', 'berlangsung',
             'berlebihan', 'bermacam', 'bermacam-macam', 'bermaksud', 'bermula', 'bersama', 'bersama-sama',
             'bersiap', 'bersiap-siap', 'bertanya', 'bertanya-tanya', 'berturut', 'berturut-turut', 'bertutur',
             'berujar', 'berupa', 'besar', 'betul',
             'betulkah', 'biasa', 'biasanya', 'bila', 'bilakah', 'bisa', 'bisakah',
             'boleh', 'bolehkah', 'bolehlah', 'buat', 'bukan', 'bukankah', 'bukanlah',
             'bukannya', 'bulan', 'bung', 'cara', 'caranya', 'cukup', 'cukupkah',
             'cukuplah', 'cuma', 'dahulu', 'dalam', 'dan', 'dapat', 'dari', 'daripada',
             'datang', 'dekat', 'demi', 'demikian', 'demikianlah', 'dengan', 'depan',
             'di', 'dia', 'diakhiri', 'diakhirinya', 'dialah', 'diantara', 'diantaranya',
             'diberi', 'diberikan', 'diberikannya', 'dibuat', 'dibuatnya', 'didapat',
             'didatangkan', 'digunakan', 'diibaratkan', 'diibaratkannya', 'diingat',
             'diingatkan', 'diinginkan', 'dijawab', 'dijelaskan', 'dijelaskannya',
             'dikarenakan', 'dikatakan', 'dikatakannya', 'dikerjakan', 'diketahui',
             'diketahuinya', 'dikira', 'dilakukan', 'dilalui', 'dilihat', 'dimaksud',
             'dimaksudkannya', 'dimaksudnya', 'diminta', 'dimintai', 'dimisalkan',
             'dimulai', 'dimulailah', 'dimulainya', 'dimungkinkan', 'dini', 'dipastikan',
             'diperbuat', 'diperbuatnya', 'dipergunakan', 'diperkirakan', 'diperlihatkan',
             'diperlukan', 'diperlukannya', 'dipersoalkan', 'dipertanyakan', 'dipunyai',
             'diri', 'dirinya', 'disampaikan', 'disebut', 'disebutkan', 'disebutkannya',
             'disini', 'disinilah', 'ditambahkan', 'ditandaskan', 'ditanya', 'ditanyai',
             'ditanyakan', 'ditegaskan', 'ditujukan', 'ditunjuk', 'ditunjuki', 'ditunjukkan',
             'ditunjukkannya', 'ditunjuknya', 'dituturkan', 'dituturkannya', 'diucapkan',
             'diucapkannya', 'diungkapkan', 'dong', 'dua', 'dulu', 'empat', 'enggak', 'enggaknya',
             'entah', 'entahlah', 'guna', 'gunakan', 'hal',
             'hampir', 'hanya', 'hanyalah', 'hari', 'harus', 'haruslah', 'harusnya',
             'hendak', 'hendaklah', 'hendaknya', 'hingga', 'ia', 'ialah', 'ibarat',
             'ibaratkan', 'ibaratnya', 'ibu', 'ikut', 'ingat', 'ingat-ingat', 'ingin',
             'inginkah', 'inginkan', 'ini', 'inikah', 'inilah', 'itu', 'itukah', 'itulah',
             'jadi', 'jadilah', 'jadinya', 'jangan', 'jangankan', 'janganlah', 'jauh', 'jawab',
             'jawaban', 'jawabnya', 'jelas', 'jelaskan', 'jelaslah', 'jelasnya', 'jika',
             'jikalau', 'juga', 'jumlah', 'jumlahnya', 'justru', 'kala', 'kalau', 'kalaulah',
             'kalaupun', 'kalian', 'kami', 'kamilah', 'kamu', 'kamulah', 'kan', 'kapan', 'kapankah',
             'kapanpun', 'karena', 'karenanya', 'kasus', 'kata', 'katakan', 'katakanlah', 'katanya',
             'ke', 'keadaan', 'kebetulan', 'kecil', 'kedua', 'keduanya', 'keinginan', 'kelamaan', 'kelihatan', 'kelihatannya',
             'kelima', 'keluar', 'kembali', 'kemudian', 'kemungkinan', 'kemungkinannya',
             'kenapa', 'kepada', 'kepadanya', 'kesampaian', 'keseluruhan', 'keseluruhannya',
             'keterlaluan', 'ketika', 'khususnya', 'kini', 'kinilah', 'kira', 'kira-kira',
             'kiranya', 'kita', 'kitalah', 'kok', 'kurang', 'lagi', 'lagian', 'lah', 'lain',
             'lainnya', 'lalu', 'lama', 'lamanya', 'lanjut', 'lanjutnya', 'lebih', 'lewat',
             'lima', 'luar', 'macam', 'maka', 'makanya', 'makin', 'malah', 'malahan', 'mampu',
             'mampukah', 'mana', 'manakala', 'manalagi', 'masa', 'masalah', 'masalahnya', 'masih',
             'masihkah', 'masing', 'masing-masing', 'mau', 'maupun', 'melainkan', 'melakukan',
             'melalui', 'melihat', 'melihatnya', 'memang', 'memastikan', 'memberi', 'memberikan',
             'membuat', 'memerlukan', 'memihak', 'meminta', 'memintakan', 'memisalkan', 'memperbuat',
             'mempergunakan', 'memperkirakan', 'memperlihatkan',
             'mempersiapkan', 'mempersoalkan', 'mempertanyakan', 'mempunyai', 'memulai',
             'memungkinkan', 'menaiki', 'menambahkan', 'menandaskan', 'menanti', 'menanti-nanti', 'menantikan',
             'menanya', 'menanyai', 'menanyakan', 'mendapat',
             'mendapatkan', 'mendatang', 'mendatangi', 'mendatangkan', 'menegaskan', 'mengakhiri', 'mengapa',
             'mengatakan', 'mengatakannya', 'mengenai', 'mengerjakan',
             'mengetahui', 'menggunakan', 'menghendaki', 'mengibaratkan', 'mengibaratkannya', 'mengingat', 'mengingatkan',
             'menginginkan', 'mengira', 'mengucapkan',
             'mengucapkannya', 'mengungkapkan', 'menjadi', 'menjawab', 'menjelaskan', 'menuju', 'menunjuk', 'menunjuki',
             'menunjukkan', 'menunjuknya', 'menurut', 'menuturkan', 'menyampaikan', 'menyangkut', 'menyatakan', 'menyebutkan',
             'menyeluruh', 'menyiapkan', 'merasa', 'mereka', 'merekalah', 'merupakan', 'meski', 'meskipun', 'meyakini',
             'meyakinkan', 'minta', 'mirip', 'misal', 'misalkan',
             'misalnya', 'mula', 'mulai', 'mulailah', 'mulanya', 'mungkin', 'mungkinkah', 'nah', 'naik', 'namun', 'nanti',
             'nantinya', 'nyaris', 'nyatanya', 'oleh', 'olehnya', 'pada', 'padahal', 'padanya', 'pak', 'paling', 'panjang',
             'pantas', 'para', 'pasti', 'pastilah', 'penting', 'pentingnya', 'per', 'percuma', 'perlu', 'perlukah', 'perlunya',
             'pernah', 'persoalan', 'pertama', 'pertama-tama', 'pertanyaan', 'pertanyakan', 'pihak', 'pihaknya', 'pukul', 'pula',
             'pun', 'punya', 'rasa', 'rasanya', 'rata', 'rupanya', 'saat', 'saatnya', 'saja', 'sajalah', 'saling', 'sama',
             'sama-sama', 'sambil', 'sampai', 'sampai-sampai', 'sampaikan', 'sana', 'sangat', 'sangatlah',
             'satu', 'saya', 'sayalah', 'se', 'sebab', 'sebabnya', 'sebagai', 'sebagaimana', 'sebagainya', 'sebagian',
             'sebaik', 'sebaik-baiknya', 'sebaiknya', 'sebaliknya', 'sebanyak', 'sebegini', 'sebegitu', 'sebelum',
             'sebetulnya', 'sebisanya', 'sebuah', 'sebut', 'sebutlah', 'sebutnya', 'secara', 'secukupnya', 'sedang',
             'sedangkan', 'sedemikian', 'sedikit',
             'sedikitnya', 'seenaknya', 'segala', 'segalanya', 'segera', 'seharusnya', 'sehingga', 'seingat',
             'sejak', 'sejauh', 'sejenak', 'sejumlah', 'sekadar', 'sekadarnya', 'sekali', 'sekali-kali', 'sekalian',
             'sekaligus', 'sekalipun', 'sekarang', 'sekarang', 'sekecil', 'seketika', 'sekiranya', 'sekitar',
             'sekitarnya', 'sekurang-kurangnya', 'sekurangnya', 'sela', 'selain', 'selaku', 'selalu', 'selama',
             'selama-lamanya', 'selamanya', 'selanjutnya', 'seluruh', 'seluruhnya', 'semacam', 'semakin', 'semampu',
             'semampunya', 'semasa', 'semasih', 'semata', 'semata-mata', 'semaunya', 'sementara', 'semisal',
             'semisalnya', 'sempat', 'semua', 'semuanya',
             'semula', 'sendiri', 'sendirian', 'sendirinya', 'seolah', 'seolah-olah', 'seorang', 'sepanjang',
             'sepantasnya', 'sepantasnyalah', 'seperlunya',
             'seperti', 'sepertinya', 'sepihak', 'sering', 'seringnya', 'serta', 'serupa', 'sesaat', 'sesama', 'sesampai',
             'sesegera', 'sesekali', 'seseorang',
             'sesuatu', 'sesuatunya', 'sesudah', 'sesudahnya', 'setelah', 'setempat', 'setengah', 'seterusnya', 'setiap',
             'setiba', 'setibanya', 'setidak-tidaknya',
             'setidaknya', 'setinggi', 'seusai', 'sewaktu', 'siap', 'siapa', 'siapakah', 'siapapun', 'sini', 'sinilah',
             'soal', 'soalnya', 'suatu', 'sudah', 'sudahkah',
             'sudahlah', 'supaya', 'tadi', 'tadinya', 'tahu', 'tahun', 'tak', 'tambah', 'tambahnya', 'tampak',
             'tampaknya', 'tandas', 'tandasnya', 'tanpa', 'tanya', 'tanyakan', 'tanyanya', 'tapi', 'tegas', 'tegasnya', 'telah', 'tempat',
             'tengah', 'tentang', 'tentu', 'tentulah', 'tentunya', 'tepat', 'terakhir', 'terasa', 'terbanyak', 'terdahulu', 'terdapat',
             'terdiri', 'terhadap', 'terhadapnya', 'teringat', 'teringat-ingat', 'terjadi', 'terjadilah', 'terjadinya', 'terkira',
             'terlalu', 'terlebih', 'terlihat', 'termasuk', 'ternyata', 'tersampaikan', 'tersebut', 'tersebutlah', 'tertentu',
             'tertuju', 'terus', 'terutama', 'tetap', 'tetapi', 'tiap', 'tiba', 'tiba-tiba', 'tidak', 'tidakkah', 'tidaklah',
             'tiga', 'tinggi', 'toh', 'tunjuk', 'turut', 'tutur', 'tuturnya', 'ucap', 'ucapnya', 'ujar', 'ujarnya', 'umum',
             'umumnya', 'ungkap', 'ungkapnya', 'untuk', 'usah', 'usai',
             'waduh', 'wah', 'wahai', 'waktu', 'waktunya', 'walau', 'walaupun', 'wong', 'yaitu', 'yakin', 'yakni', 'yang',
             'dr', 'Diterjemahkan Google', 'oleh', 'Google', 'Diterjemahkan', 'spa', 'pas', 'dgn', 'ya', 'Di', 'di', 'n',
             'Diterjemahkan', 'Google', 'ya', 'krn', 'bgt', 'Tapi', 'juga', 'jg', 'tdk', 'sih', 'dr', 'ini', 'hotel ini',
             'jd', 'Diterjemahkan', 'gak', 'u', 'tp', 'dg', 'yd', 'klo', 'kalo', 'hrs', 'hrsnya', 'nih', 'nihh', 'dah',
             'aja', 'kok', 'gak', 'ga', 'gak ada', 'mas', 'Mas', 'mba', 'Mba', 'mbak', 'Mbak', 'mbak2', 'Mbak2', 'mbak mba', 'Mbak mba',
             'sist', 'Sis', 'sis', 'Sis', 'sis2', 'Sis2', 'sis sis', 'Sis Sis', 'bro', 'Bro', 'bro bro', 'Bro Bro',
             'bro2', 'Bro2', 'bro bro', 'Bro bro', 'om', 'Om', 'om om', 'Om Om', 'om2', 'Om2', 'om om', 'Om om',
             'pak', 'Pak', 'pak pak', 'Pak Pak', 'pak2', 'Pak2', 'pak pak', 'Pak pak', 'bpk', 'Bpk', 'bpk bpk', 'Bpk Bpk', 'bpk2', 'Bpk2', 'bpk bpk', 'Bpk bpk',
             'ibu', 'Ibu', 'ibu ibu', 'Ibu Ibu', 'ibu2', 'Ibu2', 'ibu ibu', 'Ibu ibu', 'bu', 'Bu', 'bu bu', 'Bu Bu', 'bu2', 'Bu2', 'bu bu', 'Bu bu',
             'mas', 'Mas', 'mas mas', 'Mas Mas', 'mas2', 'Mas2', 'mas mas', 'Mas mas'}
    
    stopwords_en = {"the","and","to","of","in","is","it","for","on","with","this","that", 
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
            "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
            'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
            'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
            'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
            'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
            'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
            'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
            'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
            'against', 'between', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
            'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
            'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
            'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
            "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
            'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn',
            "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
            "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
            'shan', "shan't", 'shouldn', "shouldn't",
            'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
    stopwords = stopwords_id if lang == "id" else stopwords_en

    pos_counter = Counter()
    neg_counter = Counter()

    for row in rows:
        if not row["review_text"]:
            continue
        # Tokenisasi kata sederhana
        words = re.findall(r"\b\w+\b", row["review_text"].lower())
        words = [w for w in words if w not in stopwords and len(w) > 2]

        if row["sentiment_nb"] == "POSITIF":
            pos_counter.update(words)
        elif row["sentiment_nb"] == "NEGATIF":
            neg_counter.update(words)

    return {
        "positive": pos_counter.most_common(limit),
        "negative": neg_counter.most_common(limit)
    }

# Uji coba
def get_trend_sentiment(hotel_id, days=30):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT DATE(COALESCE(review_date, created_at)) AS d,
               SUM(CASE WHEN LOWER(sentiment_nb) LIKE 'posit%' THEN 1 ELSE 0 END) AS pos,
               SUM(CASE WHEN LOWER(sentiment_nb) LIKE 'negat%' THEN 1 ELSE 0 END) AS neg
        FROM sentiment_reviews
        WHERE hotel_id=%s
          AND COALESCE(review_date, created_at) >= CURDATE() - INTERVAL %s DAY
        GROUP BY d
        ORDER BY d
    """, (hotel_id, days))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows


def get_latest_sentiment(hotel_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT review_date AS time, created_at, user_name, review_text, rating, sentiment_nb, sentiment_svm
        FROM sentiment_reviews
        WHERE hotel_id=%s
        ORDER BY review_date DESC, sentiment_id DESC
        LIMIT 1
    """, (hotel_id,))
    rows = cur.fetchone()
    cur.close(); conn.close()
    return rows

def list_sentiments(hotel_id, limit=200):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT s.*, h.review_text as raw_text
        FROM sentiment_reviews s
        LEFT JOIN hotel_reviews h ON h.review_id = s.review_id
        WHERE s.hotel_id=%s
        ORDER BY s.review_date DESC
        LIMIT %s
    """, (hotel_id, limit))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

# analytics
def count_sentiments(hotel_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT sentiment_nb, COUNT(*) FROM sentiment_reviews
        WHERE hotel_id=%s
        GROUP BY sentiment_nb
    """, (hotel_id,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return {r[0]: r[1] for r in rows}

def trend_reviews(hotel_id, days=30):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT DATE(review_date) as d, COUNT(*) as cnt
        FROM sentiment_reviews
        WHERE hotel_id=%s AND review_date >= (NOW() - INTERVAL %s DAY)
        GROUP BY DATE(review_date)
        ORDER BY d
    """, (hotel_id, days))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

# subscribers
def get_subscribers():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM telegram_users ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def add_subscriber(chat_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT IGNORE INTO telegram_users (chat_id, subscribed) VALUES (%s, TRUE)", (chat_id,))
    conn.commit()
    cur.close(); conn.close()

def remove_subscriber(chat_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM telegram_users WHERE chat_id=%s", (chat_id,))
    conn.commit()
    cur.close(); conn.close()

# notifications log
def log_notification(review_id, chat_id, status, message_text=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notifications (review_id, chat_id, status, created_at) VALUES (%s,%s,%s,NOW())", (review_id, chat_id, status))
    conn.commit()
    cur.close(); conn.close()

def get_notifications(limit=None):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    base_query = """
        SELECT n.*, s.review_text, s.sentiment_nb, s.sentiment_svm
        FROM notifications n
        LEFT JOIN sentiment_reviews s ON s.review_id = n.review_id
        ORDER BY n.created_at DESC
    """
    #Tambahkan LIMIT hanya jika limit valid
    if limit is not None and int(limit) > 0:
        base_query += " LIMIT %s"
        cur.execute(base_query, (limit,))
    else:
        cur.execute(base_query)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
