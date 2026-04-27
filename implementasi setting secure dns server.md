# Implementasi Setting Secure DNS Server dan HTTPS (SSL) untuk eltekers-bogor.com

Dokumen ini berisi tahapan lengkap untuk menghubungkan domain `eltekers-bogor.com` yang berada di Hostinger (hPanel) ke VPS (`148.230.99.122`) dan mengaktifkan akses aman HTTPS menggunakan sertifikat SSL (Let's Encrypt).

Mengingat propagasi DNS dapat memakan waktu hingga 24 jam, proses ini dibagi menjadi tahapan konfigurasi yang bisa dilakukan sekarang dan aktivasi SSL yang bisa diverifikasi setelah propagasi selesai.

## Konsekuensi Penggunaan Let's Encrypt via Docker

**Keuntungan:**
1. **Lebih Bersih dan Terisolasi**: Tidak perlu menginstal Certbot langsung di OS VPS.
2. **Portabilitas Tinggi**: Konfigurasi SSL digabung ke dalam `docker-compose.yml` dan `nginx.conf`, memudahkan migrasi antar VPS.
3. **Manajemen Otomatis**: Mudah untuk ditambahkan fungsi perpanjangan otomatis (*auto-renewal*).

**Tantangan Teknis:**
1. **Kompleksitas Konfigurasi**: Memerlukan *Volume Mapping* antara container Nginx dan Certbot untuk membaca `.well-known/acme-challenge` dan `/etc/letsencrypt/`.
2. **Risiko Nginx Gagal Start**: Nginx harus diatur untuk port 80 terlebih dahulu. Jika langsung diatur port 443 sebelum sertifikat dibuat, Nginx akan gagal start.
3. **Downtime Singkat**: Akan ada jeda singkat saat me-restart Nginx setelah sertifikat pertama kali terbit.

---

## Tahapan 1: Konfigurasi DNS di Hostinger (hPanel)

Langkah-langkah berikut mengatur agar domain mengarah ke IP VPS. 

1. **Login ke Hostinger**:
   - Buka hPanel Hostinger dan login menggunakan akun Google `eltekers.digitalassistance@gmail.com`.
2. **Akses Manajemen Domain**:
   - Di dashboard utama, pilih menu **Domain**.
   - Temukan `eltekers-bogor.com` dan klik **Kelola** (Manage).
3. **Edit DNS / Nameserver**:
   - Buka menu **DNS / Nameserver** di panel sebelah kiri.
4. **Update A Record**:
   - Cari baris `A Record` dengan nama `@` (root domain).
   - Edit record tersebut dan arahkan (points to) ke IP VPS: `148.230.99.122`.
   - Simpan perubahan.
5. **Update CNAME (Opsional namun disarankan)**:
   - Cari baris `CNAME` dengan nama `www`.
   - Arahkan ke `eltekers-bogor.com` agar pengunjung yang mengetik `www` tetap bisa mengakses situs.
6. **Tunggu Propagasi**:
   - Propagasi DNS membutuhkan waktu antara 1 hingga 24 jam agar berlaku global.

## Tahapan 2: Penyesuaian Konfigurasi Server (VPS)

Sebelum HTTPS bisa diaktifkan, server VPS disiapkan untuk menerima permintaan validasi dari Let's Encrypt.

### 1. Penyesuaian Django App (`.env`)
Menambahkan domain ke daftar host yang diizinkan oleh Django agar tidak menghasilkan error 400 Bad Request.
- **File**: `.env`
- **Perubahan**: 
  ```env
  ALLOWED_HOSTS=148.230.99.122,localhost,127.0.0.1,eltekers-bogor.com,www.eltekers-bogor.com
  ```

### 2. Penyesuaian Docker (`docker-compose.yml`)
Menambahkan service certbot dan memetakan volume sertifikat ke Nginx.
- **Perubahan**:
  - Tambahkan container `certbot`.
  - Mapping volume `/etc/letsencrypt` dan `/var/www/certbot`.
  - Buka port 443 di container Nginx.

### 3. Penyesuaian Nginx (`nginx/nginx.conf`)
Menyiapkan Nginx untuk melayani tantangan webroot Certbot.
- **Perubahan**:
  - Ganti `server_name` menjadi `eltekers-bogor.com www.eltekers-bogor.com`.
  - Tambahkan lokasi routing untuk `/.well-known/acme-challenge/`.

## Tahapan 3: Generate Sertifikat SSL (Setelah Propagasi Selesai)

Setelah domain berhasil dipropagasi dan mengarah sepenuhnya ke VPS, jalankan perintah berikut di server VPS:

1. Request sertifikat pertama kali (Jalankan via terminal VPS):
   ```bash
   docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d eltekers-bogor.com -d www.eltekers-bogor.com --email eltekers.digitalassistance@gmail.com --agree-tos --no-eff-email
   ```
2. Sesuaikan `nginx.conf` untuk menggunakan sertifikat SSL (HTTPS/Port 443).
3. Restart Nginx agar menerapkan HTTPS:
   ```bash
   docker compose restart nginx
   ```
4. Verifikasi bahwa akses ke `http://eltekers-bogor.com` otomatis ter-redirect ke `https://eltekers-bogor.com` dan muncul indikator gembok (Secure).
