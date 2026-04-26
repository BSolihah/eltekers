# Gunakan image Python resmi versi 3.9
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Buat direktori kerja di dalam container
WORKDIR /app

# Install dependensi sistem yang dibutuhkan (misal untuk PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Salin file requirements dan install dependensi Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install gunicorn python-dotenv psycopg2-binary

# Salin seluruh kode proyek ke direktori kerja
COPY . /app/

# Port yang akan diekspos oleh container
EXPOSE 8000

# Perintah default untuk menjalankan aplikasi menggunakan Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "eltekers.wsgi:application"]
