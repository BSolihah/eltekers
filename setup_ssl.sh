#!/bin/bash

# Pastikan script dijalankan di direktori project (tempat docker-compose.yml berada)
echo "Memulai proses setup SSL untuk eltekers-bogor.com..."

# 1. Request sertifikat Let's Encrypt (Webroot method)
# Nginx harus sudah berjalan dan listen di port 80 untuk melayani /.well-known/acme-challenge/
echo "Me-request sertifikat SSL Let's Encrypt..."
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d eltekers-bogor.com -d www.eltekers-bogor.com --email eltekers.digitalassistance@gmail.com --agree-tos --no-eff-email

if [ $? -eq 0 ]; then
    echo "Sertifikat berhasil dibuat."
    
    # 2. Mengganti nginx.conf dengan nginx-ssl.conf
    echo "Mengganti konfigurasi Nginx untuk menggunakan port 443 (SSL)..."
    cp nginx/nginx-ssl.conf nginx/nginx.conf
    
    # 3. Restart container nginx untuk menerapkan konfigurasi baru
    echo "Me-restart container Nginx..."
    docker compose restart nginx
    
    echo "Proses deploy SSL selesai! Silakan cek https://eltekers-bogor.com di browser."
else
    echo "Gagal membuat sertifikat. Silakan periksa pesan error di atas."
    echo "Pastikan domain eltekers-bogor.com sudah mengarah ke IP VPS Anda."
fi
