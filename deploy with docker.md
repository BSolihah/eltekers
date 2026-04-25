# Panduan Deployment Produksi dengan Docker

Dokumen ini menjelaskan langkah-langkah untuk melakukan deployment aplikasi **EIS Bogor** ke server produksi menggunakan arsitektur **Docker** dan **Docker Compose**. 

Pendekatan ini jauh lebih modern, mudah, dan *scalable* karena semua layanan (Django, PostgreSQL, Redis, dan Nginx) dijalankan di dalam *container* yang terisolasi.

---

## 1. Komponen yang Telah Disiapkan
Untuk mendukung arsitektur Docker, beberapa file telah ditambahkan ke repositori proyek:
1.  **`Dockerfile`**: Resep untuk membangun *image* aplikasi Django Anda.
2.  **`docker-compose.yml`**: File orkestrasi untuk menjalankan seluruh layanan secara bersamaan (`db`, `redis`, `web`, `nginx`).
3.  **`nginx/nginx.conf`**: Konfigurasi Nginx untuk bertindak sebagai *reverse proxy* dan melayani file statis (`/static/`) serta file media (`/media/`).
4.  **`.dockerignore`**: File untuk mencegah file lokal (seperti `venv` atau `db.sqlite3` lokal) masuk ke dalam *container*.

---

## 2. Persiapan di Server Produksi
Pastikan server Anda (Ubuntu/Debian/CentOS) sudah memiliki **Docker** dan **Docker Compose** terinstal.

Jika belum, Anda bisa menginstalnya dengan perintah (untuk Ubuntu):
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 3. Langkah-Langkah Deployment

### A. Unduh Proyek
Clone repositori proyek Anda ke server:
```bash
cd /home/user/
git clone https://github.com/BSolihah/eltekers.git eisbogor
cd eisbogor
```

### B. Siapkan Variabel Lingkungan (.env)
Buat file `.env` di direktori utama (`/home/user/eisbogor/`). File ini akan otomatis dibaca oleh `docker-compose`.
```bash
# Isi file .env
DEBUG=False
SECRET_KEY=ganti-dengan-key-rahasia-anda
ALLOWED_HOSTS=domainanda.com,localhost,127.0.0.1
```
*Catatan: Konfigurasi URL database dan Redis sudah diatur secara otomatis di dalam `docker-compose.yml` untuk saling terhubung antar container.*

### C. Jalankan Deployment
Jalankan perintah ini di dalam folder proyek untuk mengunduh image, membangun image Django, mengumpulkan file statis, menjalankan migrasi database, dan menyalakan semua server:
```bash
sudo docker-compose up -d --build
```
Keterangan:
*   `-d`: Menjalankan layanan di latar belakang (*detached mode*).
*   `--build`: Memaksa pembangunan ulang image Django jika ada perubahan kode.

### D. Verifikasi
Pastikan semua container berjalan (status `Up`):
```bash
sudo docker-compose ps
```
Aplikasi Anda sekarang seharusnya bisa diakses melalui web browser dengan memasukkan alamat IP server atau domain Anda.

---

## 4. Manajemen Aplikasi Sehari-hari

**Melihat Log Aplikasi (Mencari Error):**
```bash
sudo docker-compose logs -f web
```

**Mematikan Aplikasi:**
```bash
sudo docker-compose down
```

**Memasuki Container Django (Untuk membuat superuser baru, dll):**
```bash
sudo docker-compose exec web bash
# Setelah di dalam container, Anda bisa menjalankan perintah manage.py:
# python manage.py createsuperuser
```

**Memperbarui Aplikasi Setelah Mengubah Kode (Git Pull):**
```bash
git pull origin main
sudo docker-compose up -d --build
```

---

## Catatan Penting Mengenai Database
Deployment Docker ini menggunakan **PostgreSQL** (container `db`) alih-alih `sqlite3` bawaan untuk performa produksi yang jauh lebih baik. Karena ini adalah database baru di dalam container, data lama di `db.sqlite3` lokal Anda tidak akan terbawa. Anda perlu membuat akun Admin Daerah / Superuser baru setelah container menyala.
