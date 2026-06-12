FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for MySQL client libraries.
RUN apt-get update && apt-get install -y \
    gcc \
    mariadb-client-compat \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway injects PORT at runtime. Docker Compose uses the default 5000.
EXPOSE 5000

ENV FLASK_APP=app.py
ENV PORT=5000
ENV DATA_DIR=/tmp
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os, requests; requests.get(f'http://127.0.0.1:{os.getenv(\"PORT\", \"5000\")}/health', timeout=5).raise_for_status()"

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers ${WEB_CONCURRENCY:-1} --threads ${GUNICORN_THREADS:-4} --worker-class gthread --timeout ${GUNICORN_TIMEOUT:-120} app:app"]
