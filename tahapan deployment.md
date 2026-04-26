# Panduan Deployment Produksi: Django + Gunicorn + Nginx

Dokumen ini berisi tahapan lengkap untuk mendeploy aplikasi **EIS Bogor** ke server produksi berbasis Linux (Ubuntu/Debian) menggunakan Gunicorn dan Nginx (Non-Docker).

---

## 1. Persiapan Infrastruktur Server
Instalasi paket-paket sistem yang diperlukan:
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx redis-server git libpq-dev
```

Pastikan layanan Redis aktif:
```bash
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

---

## 2. Pengaturan Variabel Lingkungan (.env)
Aplikasi telah dikonfigurasi untuk membaca variabel dari file `.env`. Buat file tersebut di root folder proyek:
```bash
# File: /home/user/eisbogor/.env

DEBUG=False
SECRET_KEY=ganti-dengan-key-rahasia-anda
ALLOWED_HOSTS=domainanda.com,IP_SERVER
DATABASE_URL=postgres://user:password@localhost:5432/dbname
REDIS_URL=redis://127.0.0.1:6379/1
```

---

## 3. Instalasi Aplikasi di Server
Clone kode dan siapkan lingkungan Python:
```bash
cd /home/user
git clone https://github.com/BSolihah/eltekers.git eisbogor
cd eisbogor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn python-dotenv
```

Persiapkan database dan file statis:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 4. Konfigurasi Gunicorn (Application Server)
Gunakan Systemd untuk mengelola proses Gunicorn:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Isi file dengan konfigurasi berikut:
```ini
[Unit]
Description=gunicorn daemon untuk EIS Bogor
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/user/eisbogor
ExecStart=/home/user/eisbogor/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          eltekers.wsgi:application

[Install]
WantedBy=multi-user.target
```

Aktifkan service:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## 5. Konfigurasi Nginx (Reverse Proxy)
Buat konfigurasi situs Nginx baru:
```bash
sudo nano /etc/nginx/sites-available/eisbogor
```

Gunakan konfigurasi berikut:
```nginx
server {
    listen 80;
    server_name domainanda.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/user/eisbogor/static/;
    }

    location /media/ {
        alias /home/user/eisbogor/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Aktifkan dan restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/eisbogor /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## 6. SSL / HTTPS (Opsional tapi Direkomendasikan)
Gunakan Certbot untuk mengamankan koneksi:
```bash
sudo apt install python3-certbot-nginx
sudo certbot --nginx -d domainanda.com
```

---

## Checklist Akhir
- [ ] Pastikan folder `media/` dan `static/` memiliki permission yang tepat agar bisa dibaca oleh Nginx.
- [ ] Verifikasi Redis berjalan dengan `redis-cli ping`.
- [ ] Cek log gunicorn jika terjadi error: `sudo journalctl -u gunicorn`.
