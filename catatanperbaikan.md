# Catatan Perbaikan Sistem - 27 April 2026

## 1. Perbaikan Registrasi Peserta (Fail-Safe Account Creation)
**Masalah:**
- Peserta gagal dibuat karena pelanggaran batasan `NOT NULL` pada kolom `berat_badan` dan `tinggi_badan` saat input kosong.
- Akun (`Account`) tetap tersimpan meskipun profil `Peserta` gagal, menyebabkan error "Username sudah digunakan" saat mencoba mendaftar ulang.

**Perbaikan:**
- Menggunakan `django.db.transaction.atomic()` pada `register_view` di `sasana/views.py`. Jika pembuatan profil `Peserta` gagal, maka pembuatan `Account` akan otomatis di-rollback.
- Menambahkan validasi/defaulting pada `berat_badan` dan `tinggi_badan` agar jika menerima string kosong atau `None` dari frontend, akan diubah menjadi `0` sebelum disimpan ke database.

## 2. Perbaikan Aplikasi Hang Saat Login
**Masalah:**
- Aplikasi mengalami hang saat login karena `SESSION_ENGINE` yang menggunakan `django.contrib.sessions.backends.cache` mencoba menghubungi Redis yang tidak aktif tanpa adanya timeout.
- Tidak ada mekanisme fallback jika Redis bermasalah.

**Perbaikan:**
- Menambahkan parameter `SOCKET_CONNECT_TIMEOUT` dan `SOCKET_TIMEOUT` (1 detik) pada konfigurasi `CACHES` di `eltekers/settings.py`.
- Mengubah `SESSION_ENGINE` menjadi `django.contrib.sessions.backends.cached_db`.
- **Manfaat:** Sistem akan mencoba menggunakan Redis untuk session, namun jika gagal (timeout), akan otomatis beralih menggunakan database SQLite (fallback), sehingga proses login tidak lagi menggantung.

---
*Catatan: Perubahan ini memastikan integritas data pada saat pendaftaran dan stabilitas sistem saat layanan eksternal (seperti Redis) sedang tidak tersedia.*
