# 🐳 LOCAL DOCKER TESTING GUIDE

Panduan untuk testing Docker image aplikasi secara lokal sebelum deploy ke Railway.

---

## 📋 PREREQUISITES

Pastikan sudah installed:

- ✅ Docker Desktop (Windows/Mac) atau Docker (Linux)
- ✅ Docker running dan dapat diakses
- ✅ Terminal/Command Prompt
- ✅ Git dengan repository terkini

---

## 🔍 VERIFY DOCKER INSTALLATION

```bash
# Check Docker version
docker --version

# Output should be:
# Docker version 29.4.2 (atau lebih tinggi)

# Check Docker daemon running
docker ps

# If error: Docker daemon not running
# Solution: Start Docker Desktop (Windows/Mac) atau systemctl start docker (Linux)
```

---

## 🏗️ BUILD DOCKER IMAGE LOCALLY

### **Step 1: Navigate to Project Directory**

```bash
cd "d:\PROYEK TUGAS AKHIR\APP TA"
# atau untuk Linux/Mac:
cd ~/PROYEK\ TUGAS\ AKHIR/APP\ TA
```

### **Step 2: Build Image**

```bash
# Build dengan tag
docker build -t hotel-sentiment:test .

# Expected output:
# [+] Building 45.2s (15/15) FINISHED
# => importing cache manifest from docker.io/library/buildkit:latest
# => [internal] load build definition
# ...
# => => naming to docker.io/library/hotel-sentiment:test
```

**Build time:** 5-10 menit untuk first build (tergantung internet speed)

### **Step 3: Verify Image Built Successfully**

```bash
# List images
docker images | grep hotel-sentiment

# Output:
# REPOSITORY           TAG    IMAGE ID      CREATED      SIZE
# hotel-sentiment      test   a1b2c3d4e5f6  2 min ago    890MB
```

---

## 🚀 RUN CONTAINER LOCALLY

### **Option A: Quick Test (Tanpa Database)**

```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e SECRET_KEY=test-secret-key-12345 \
  hotel-sentiment:test
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: off
 * WARNING: This is a development server. Do not use in production.
```

**Test akses:**
```bash
curl http://localhost:5000/health

# Response:
# {
#   "status": "degraded",  (karena belum ada DB)
#   "timestamp": "2026-06-08T...",
#   "services": {
#     "database": "error"
#   }
# }
```

### **Option B: Full Test (Dengan Docker Compose + MySQL)**

**1. Create docker-compose.yml di project root:**

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: hotel-sentiment-app
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: development
      SECRET_KEY: dev-secret-key-123456789
      DB_HOST: mysql
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: rootpassword
      DB_NAME: monitoring_review
      SERPAPI_KEY: "3bea6306886c2e5dea2281bc68bca9cd9908b182974a843f4cf9798fe1d3eb01"  # Add your key if want full test
    depends_on:
      - mysql
    volumes:
      - ./:/app  # Live reload code changes
    networks:
      - hotel-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  mysql:
    image: mysql:8.0
    container_name: hotel-sentiment-mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: monitoring_review
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql
    networks:
      - hotel-net
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mysql_data:

networks:
  hotel-net:
    driver: bridge
```

**2. Run full stack:**

```bash
docker-compose up --build

# Expected output:
# Creating hotel-sentiment-mysql ... done
# Creating hotel-sentiment-app   ... done
# ...
# hotel-sentiment-app   |  * Running on http://0.0.0.0:5000
```

**3. Test full stack:**

```bash
# Test health check (sekarang database should connected)
curl http://localhost:5000/health

# Expected response:
{
  "status": "healthy",
  "services": {
    "database": "connected"
  }
}

# Test login page
curl http://localhost:5000/login

# Test API
curl http://localhost:5000/api/notifications
```

**4. View logs:**

```bash
# Semua services
docker-compose logs -f

# Only app
docker-compose logs -f app

# Only MySQL
docker-compose logs -f mysql
```

**5. Stop services:**

```bash
docker-compose down

# Remove volumes jika mau clean
docker-compose down -v
```

---

## ✅ LOCAL TESTING CHECKLIST

Run this checklist untuk memastikan image siap untuk deployment:

- [ ] Docker image build successful
- [ ] Container start tanpa error
- [ ] Health check endpoint responsive
- [ ] Flask app running di port 5000
- [ ] MySQL connection works (jika full test)
- [ ] Database schema imported
- [ ] Tidak ada module import errors di logs
- [ ] Environment variables properly loaded
- [ ] No warnings/errors di startup

---

## 🐛 TROUBLESHOOTING LOCAL DOCKER

### **Problem: Docker daemon not running**

```
Error: "Cannot connect to Docker daemon"

Solutions:
1. Windows/Mac: Start Docker Desktop
2. Linux: sudo systemctl start docker
3. Verify: docker ps
```

### **Problem: Port 5000 already in use**

```
Error: "Address already in use"

Solutions:
1. Kill existing process:
   # Windows:
   netstat -ano | findstr :5000
   taskkill /PID [PID] /F
   
   # Linux/Mac:
   lsof -i :5000
   kill -9 [PID]

2. Use different port:
   docker run -p 5001:5000 hotel-sentiment:test
```

### **Problem: Out of Disk Space**

```
Error: "No space left on device"

Solutions:
1. Clean Docker:
   docker system prune -a
   docker volume prune
   
2. Remove old images:
   docker rmi hotel-sentiment:test
```

### **Problem: MySQL connection failed in docker-compose**

```
Error: "Cannot connect to MySQL server"

Solutions:
1. Check MySQL is running:
   docker-compose logs mysql
   
2. Wait longer for MySQL startup:
   - MySQL need 20-30 seconds untuk fully initialize
   - app service has "depends_on" dan "healthcheck"
   
3. Rebuild:
   docker-compose down -v
   docker-compose up --build
```

### **Problem: Module import errors**

```
Error: "ModuleNotFoundError: No module named 'xxx'"

Solutions:
1. Update requirements.txt
2. Rebuild image:
   docker build --no-cache -t hotel-sentiment:test .
3. Check file is in repository
```

---

## 📊 USEFUL DOCKER COMMANDS

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View images
docker images

# Remove image
docker rmi hotel-sentiment:test

# Run interactive shell
docker run -it hotel-sentiment:test /bin/bash

# View container logs
docker logs [container-id/name] -f

# Inspect container
docker inspect [container-id/name]

# Stop container
docker stop [container-id/name]

# Remove container
docker rm [container-id/name]

# Build with no cache (force rebuild)
docker build --no-cache -t hotel-sentiment:test .

# Push to Docker Hub (if registered)
docker tag hotel-sentiment:test [username]/hotel-sentiment:test
docker push [username]/hotel-sentiment:test
```

---

## 🚀 AFTER LOCAL TESTING: READY TO DEPLOY

Jika semua local test sukses:

1. ✅ Commit changes ke Git
   ```bash
   git add .
   git commit -m "test: verify docker build and local deployment"
   git push origin main
   ```

2. ✅ Go to Railway and deploy
   - Railway auto-detect Dockerfile
   - Build image (same as local)
   - Deploy container

3. ✅ Monitor Railway logs
   - Verify deployment successful
   - Check health check passing

---

## 🔍 PERFORMANCE TUNING (Optional)

Jika aplikasi terlalu slow saat local test:

```bash
# Modify Dockerfile ENTRYPOINT untuk tuning:
# Reduce workers untuk development:
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "app:app"]

# Increase for production (Railway defaults):
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--worker-class", "gthread", "--timeout", "120", "app:app"]
```

---

## 📞 GETTING HELP

Jika ada error saat local testing:

1. Check Docker logs:
   ```bash
   docker logs [container-name] -f
   ```

2. Enter container:
   ```bash
   docker exec -it [container-name] /bin/bash
   ```

3. Check Railway docs:
   - https://docs.railway.app

4. Check Docker docs:
   - https://docs.docker.com

---

**Happy Testing! 🚀**

Last Updated: 2026-06-08
