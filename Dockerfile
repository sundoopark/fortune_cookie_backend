FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

# Copy the shared app code
COPY app /app


ENV PORT=80
ENV PYTHONUNBUFFERED=1

EXPOSE $PORT

# Start Flask app with Gunicorn
CMD ["gunicorn", "app.app:app", "-b", "0.0.0.0:80", "--timeout", "120", "--worker-class", "gevent", "--workers", "2", "--capture-output", "--log-level", "debug"]