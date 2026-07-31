# 🚀 DEPLOYMENT GUIDE - Hotel Review Sentiment Monitoring

Panduan lengkap untuk men-deploy aplikasi Hotel Review Sentiment Monitoring ke production menggunakan Railway.

---

## 📋 TABLE OF CONTENTS

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Persiapan Lokal](#persiapan-lokal)
3. [Setup Railway](#setup-railway)
4. [Environment Variables](#environment-variables)
5. [Database Migration](#database-migration)
6. [Deployment Process](#deployment-process)
7. [Post-Deployment](#post-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Monitoring & Maintenance](#monitoring--maintenance)
10. [Rollback Plan](#rollback-plan)

---

## ✅ PRE-DEPLOYMENT CHECKLIST

Pastikan semua ini sudah disiapkan sebelum deploy:

- [ ] Git repository sudah setup (GitHub/GitLab)
- [ ] `.env.example` sudah diupdate dengan semua variables
- [ ] `requirements.txt` sudah optimized (dengan Gunicorn)
- [ ] `Dockerfile` sudah dibuat dan tested
- [ ] `.railwayignore` sudah dikonfigurasi
- [ ] `railway.json` sudah ada
- [ ] `app.py` sudah punya `/health` endpoint
- [ ] `schema.sql` sudah updated dengan database structure
- [ ] SerpAPI key sudah siap (untuk scraping)
- [ ] Telegram Bot token siap (optional, untuk notifikasi)

---

## 🔧 PERSIAPAN LOKAL

### 1. **Verifikasi Git Repository**

```bash
cd "d:\PROYEK TUGAS AKHIR\APP TA"
git status
git log --oneline -5  # Lihat commit terakhir
```

### 2. **Commit Perubahan Deployment**

```bash
git add Dockerfile .railwayignore railway.json requirements.txt .env.example
git commit -m "chore: add Railway deployment configuration

- Add Dockerfile for production build
- Add .railwayignore to exclude unnecessary files
- Add railway.json configuration
- Optimize requirements.txt with Gunicorn
- Add health check endpoints
- Update .env.example with Railway settings"

git push origin main
```

### 3. **Verify di Repository**

Pastikan di GitHub sudah ada:
- `Dockerfile`
- `.railwayignore`
- `railway.json`
- Updated `requirements.txt`
- Health check di `app.py`

```bash
# Test locally build Docker image (OPTIONAL tapi recommended)
docker build -t hotel-sentiment:latest .
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e DB_HOST=localhost \
  hotel-sentiment:latest
```

---

## 🛤️ SETUP RAILWAY

### **1. Create Railway Account**

1. Buka https://railway.app
2. Klik "Start a New Project"
3. Login dengan GitHub (recommended)

### **2. Create Project di Railway**

```
Actions:
1. Klik "Deploy from GitHub repo"
2. Authorize Railway untuk akses GitHub
3. Select repository: "system-sentiment-monitoring-reviews"
4. Select branch: "main"
5. Klik "Deploy"
```

Railway akan mulai initial build. Tunggu~

### **3. Add MySQL Service**

```
Actions:
1. Di project dashboard, klik "Add Service"
2. Select "MySQL"
3. Railway akan create MySQL instance
4. Copy credentials yang di-generate (untuk next step)
```

**Simpan credentials ini:**
```
DB_HOST: railway.internal
DB_PORT: 3306
DB_USER: root
DB_PASSWORD: [auto-generated, ada di MySQL service variables]
DB_NAME: [kita buat di step berikutnya]
```

### **4. Configure Environment Variables**

Di Railway dashboard → Project → Variables panel, tambahkan semua ini:

| Variable | Value | Notes |
|----------|-------|-------|
| `FLASK_ENV` | `production` | REQUIRED - untuk security |
| `SECRET_KEY` | [Generate di bawah] | REQUIRED - random 32 char |
| `APP_HOST` | `0.0.0.0` | Default Railway |
| `APP_PORT` | `5000` | Default Flask |
| `DB_HOST` | `railway.internal` | Railway internal DNS |
| `DB_PORT` | `3306` | MySQL default |
| `DB_USER` | `root` | Railway default |
| `DB_PASSWORD` | [Copy dari MySQL service] | Auto-generated |
| `DB_NAME` | `monitoring_review` | Create manually di step 5 |
| `SERPAPI_KEY` | [Your SerpAPI key] | REQUIRED - untuk scraping |
| `TELEGRAM_BOT_TOKEN` | [Your bot token] | OPTIONAL - untuk notifikasi |
| `MIN_SCRAPE_INTERVAL_SEC` | `30` | Default |
| `DATA_DIR` | `./data` | Working directory |

**Cara generate SECRET_KEY:**

```python
# Di terminal lokal:
python -c "import secrets; print(secrets.token_hex(32))"

# Output contoh:
# a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e
```

### **5. Setup MySQL Database**

**Opsi A: Gunakan Railway Database UI (Paling Mudah)**

```
1. Di Railway, buka MySQL service
2. Klik "Database" tab
3. Klik "Run Query"
4. Copy-paste seluruh isi file schema.sql
5. Klik "Execute"
```

**Opsi B: Gunakan MySQL Client (Terminal)**

```bash
# Install MySQL client jika belum
# Windows: Download dari https://dev.mysql.com/downloads/
# Mac: brew install mysql-client
# Linux: sudo apt install mysql-client

# Connect ke Railway MySQL
mysql -h [DB_HOST] \
  -u [DB_USER] \
  -p[DB_PASSWORD] \
  -e "CREATE DATABASE IF NOT EXISTS monitoring_review;"

# Import schema
mysql -h [DB_HOST] \
  -u [DB_USER] \
  -p[DB_PASSWORD] \
  monitoring_review < schema.sql

# Verify
mysql -h [DB_HOST] \
  -u [DB_USER] \
  -p[DB_PASSWORD] \
  monitoring_review -e "SHOW TABLES;"
```

**Opsi C: Gunakan GUI Tool (DBeaver)**

1. Download DBeaver Community Edition
2. Create new connection:
   - Driver: MySQL
   - Host: [DB_HOST dari Railway]
   - Username: root
   - Password: [copy dari Railway]
   - Database: monitoring_review
3. Right-click database → SQL Script → Execute script
4. Pilih file `schema.sql`

---

## 🔐 ENVIRONMENT VARIABLES (Detail)

### **Required Variables**

```
FLASK_ENV=production
SECRET_KEY=<generated-32-char-hex>
SERPAPI_KEY=<your-serpapi-api-key>
DB_HOST=railway.internal
DB_PORT=3306
DB_USER=root
DB_PASSWORD=<auto-generated-railway>
DB_NAME=monitoring_review
```

### **Optional Variables**

```
TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>  # Untuk notifikasi
```

### **Runtime Variables (Default OK)**

```
APP_HOST=0.0.0.0
APP_PORT=5000
MIN_SCRAPE_INTERVAL_SEC=30
DATA_DIR=./data
```

---

## 🗄️ DATABASE MIGRATION

### **Struktur Database**

Aplikasi ini memerlukan table berikut (dari `schema.sql`):

- `users` - Untuk akun user/admin
- `hotels` - Data hotel yang di-monitor
- `reviews` - Review dari Google Maps
- `subscribers` - Subscriber Telegram per hotel
- `scrape_jobs` - History scraping tasks

### **Verifikasi Setup Database**

```bash
mysql -h [HOST] -u [USER] -p[PASSWORD] monitoring_review

# Di MySQL CLI:
SHOW TABLES;
DESCRIBE users;
DESCRIBE hotels;
DESCRIBE reviews;
DESCRIBE subscribers;
DESCRIBE scrape_jobs;
```

---

## 🚀 DEPLOYMENT PROCESS

### **Step 1: Monitor Build**

Di Railway dashboard:

```
1. Buka project > Deployments
2. Watch the build log
3. Expected logs:
   ✓ Installing dependencies (pip install -r requirements.txt)
   ✓ Building container
   ✓ Pushing to registry
   ✓ Starting container
   ✓ Health check passing
```

**Build time:** Biasanya 5-10 menit untuk first build

### **Step 2: Verify Deployment**

```bash
# Test health check endpoint
curl https://<your-railway-domain>/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-06-08T10:30:45.123456+00:00",
  "version": "1.0.0",
  "services": {
    "app": "running",
    "database": "connected",
    "scheduler": "active"
  }
}
```

### **Step 3: Check Logs**

```
1. Railway > Logs tab
2. Lihat aplikasi startup:
   - Flask app initialized
   - Database connected
   - Scheduler started
   - Listening on port 5000
```

### **Step 4: Access Aplikasi**

```
1. Buka browser
2. Kunjungi: https://<your-railway-domain>
3. Coba login dengan test account:
   - Username: test / Password: test
   - Atau register akun baru
```

---

## 📤 POST-DEPLOYMENT

### **1. Setup Custom Domain (Optional)**

```
1. Di Railway > Settings
2. Pilih "Custom Domain"
3. Masukkan domain Anda
4. Update DNS records sesuai instruksi
```

### **2. Enable Monitoring & Alerts (Recommended)**

```
1. Railway > Settings > Metrics
2. Enable: CPU, Memory, Network monitoring
3. Setup alerts untuk:
   - Memory usage > 70%
   - Restart count > 5 in 24h
   - Health check failures
```

### **3. Setup Automated Backups (Database)**

```
1. Railway > MySQL Service > Settings
2. Enable: Automated backups
3. Backup schedule: Daily at 02:00 UTC
```

### **4. Test Fitur-Fitur Utama**

```
Test Checklist:
☐ User registration & login
☐ Dashboard loading dengan smooth
☐ Hotel data management
☐ Google Maps scraping
☐ Sentiment prediction
☐ CSV/Excel export
☐ Telegram notifications (jika enabled)
☐ Admin panel access
```

### **5. Enable HTTPS (Auto)**

Railway otomatis setup HTTPS dengan Let's Encrypt. Tidak perlu setup manual.

---

## 🔍 TROUBLESHOOTING

### **Problem: Build Failed**

```
Error: "Could not build image"

Solutions:
1. Check requirements.txt - ada typo?
2. Verify Dockerfile syntax
3. Railway logs > check specific error
4. Test docker build locally:
   docker build -t test .
5. Push fix ke GitHub, Railway akan rebuild otomatis
```

### **Problem: Application Crashes**

```
Error: "Health check failing" atau app restart loop

Debugging:
1. Railway > Logs tab
2. Cari error message spesifik
3. Common issues:
   ✗ DB connection failed: cek DB_HOST, DB_PASSWORD
   ✗ Missing SERPAPI_KEY: add di Variables
   ✗ Module not found: cek requirements.txt
4. Fix, commit, push → Railway rebuild
```

### **Problem: Database Connection Error**

```
Error: "Cannot connect to database"

Solutions:
1. Verify DATABASE IS created:
   mysql -h [HOST] -u [USER] -p[PASSWORD] -e "SHOW DATABASES;"
   
2. Check DB variables di Railway:
   - DB_HOST=railway.internal (jangan gunakan public IP)
   - DB_PORT=3306
   - DB_PASSWORD: copy exact dari MySQL service
   
3. Test connection dari app:
   curl https://<domain>/health
   - Check "database" field di response
   
4. If still failed:
   - Restart MySQL service
   - Check Railway support
```

### **Problem: Out of Memory**

```
Error: 502 Bad Gateway, "Memory limit exceeded"

Solutions:
1. Upgrade Railway plan (naik resources)
   Railway > Settings > Plan
   
2. Optimize application:
   - Increase Gunicorn workers: 2 → 1 (di Dockerfile)
   - Reduce concurrent requests
   
3. Monitor memory usage:
   Railway > Metrics tab
```

### **Problem: Slow Response**

```
Symptoms: Website/API lambat

Debugging:
1. Check database performance:
   - mysql slow log
   - Add indexes ke review table
   
2. Check model loading:
   - MODEL = ModelPredict() loading di startup
   - Cek ukuran model files (~50-100MB)
   
3. Optimize Gunicorn:
   Dockerfile ENTRYPOINT
```

### **Problem: Health Check 503**

```
Status: "degraded", database: "error"

Causes & Solutions:
1. MySQL service not running:
   Railway > MySQL service > restart
   
2. DB credentials wrong:
   Railway > App Variables > check DB_PASSWORD
   
3. Database schema not initialized:
   Run schema.sql import kembali
```

---

## 📊 MONITORING & MAINTENANCE

### **Daily Checks (Automated via Railway)**

```
Railway > Metrics:
- CPU usage: Harus < 50% normal
- Memory: Harus < 60% normal  
- Network: Monitor incoming/outgoing
- Response time: Target < 1s
```

### **Weekly Checks (Manual)**

```
1. Check application logs untuk errors
   Railway > Logs, filter last 7 days
   
2. Database size:
   SELECT table_schema, ROUND(SUM(data_length+index_length)/1024/1024,0) 
   FROM information_schema.tables 
   GROUP BY table_schema;
   
3. Review user activity
   SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
```

### **Monthly Maintenance**

```
1. Database optimization:
   OPTIMIZE TABLE reviews, users, hotels;
   
2. Clear old scraping logs:
   DELETE FROM reviews WHERE created_at < DATE_SUB(NOW(), INTERVAL 6 MONTH);
   
3. Review & update dependencies:
   pip list --outdated
   
4. Check security updates
```

### **Backup & Recovery**

```
Manual Backup:
mysqldump -h [HOST] -u [USER] -p[PASSWORD] monitoring_review > backup.sql

Restore:
mysql -h [HOST] -u [USER] -p[PASSWORD] monitoring_review < backup.sql

Railway Auto-backup:
- Location: MySQL service settings
- Frequency: Daily
- Retention: 7 days
```

---

## 🔄 ROLLBACK PLAN

Jika ada masalah setelah deploy:

### **Option 1: Revert Code**

```bash
git log --oneline  # Lihat commit sebelumnya
git revert HEAD     # Revert commit terakhir
git push origin main

# Railway akan auto-redeploy dengan versi lama
```

### **Option 2: Restart Deployment**

```
Railway > Deployments > klik deployment lama > "Redeploy"
```

### **Option 3: Database Rollback**

Jika ada data corruption:

```bash
# Restore dari backup
mysql -h [HOST] -u [USER] -p[PASSWORD] monitoring_review < backup.sql

# Atau gunakan Railway backup UI
```

---

## 📞 SUPPORT & RESOURCES

### **Documentation**

- [Railway Docs](https://docs.railway.app)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn](https://gunicorn.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### **Helpful Commands**

```bash
# Check Railway CLI status
railway status

# View logs
railway logs

# Set variable
railway variables set VARIABLE_NAME value

# Connect to Railway shell
railway shell
```

### **Contact Support**

- Railway Support: https://discord.gg/railway
- GitHub Issues: [Your repo]
- Email: [Your email]

---

## 🎯 DEPLOYMENT CHECKLIST (FINAL)

Sebelum production release:

- [ ] Semua endpoint tested
- [ ] Health check berjalan
- [ ] Database connected dan terverifikasi
- [ ] Environment variables lengkap
- [ ] HTTPS enabled
- [ ] Database backups enabled
- [ ] Monitoring & alerts setup
- [ ] Error logging configured
- [ ] Performance acceptable
- [ ] Security review passed

---

**Last Updated:** 2026-06-08  
**Version:** 1.0.0  
**Status:** Ready for Production ✅
