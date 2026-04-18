# Rancangan Front-End: Sistem Manajemen Sasana Eltekers

Dokumen ini merinci spesifikasi antarmuka pengguna (UI/UX) untuk aplikasi Sistem Manajemen Sasana menggunakan Vue.js dan Bootstrap.

## Batasan Pengguna & Panduan Aksesibilitas (UI/UX)
Sebagian besar pengguna aplikasi ini adalah kelompok **pra-manula dan manula dengan rentang usia antara 40 s.d. 58 tahun**. Oleh karena itu, rancangan antarmuka harus mematuhi panduan aksesibilitas berikut:
- **Ukuran Font Lebih Besar**: Gunakan ukuran font dasar yang lebih besar (minimal 16px) agar teks mudah dibaca tanpa harus menyipitkan mata.
- **Kontras Warna Tinggi**: Pastikan teks memiliki kontras yang jelas terhadap latar belakang. Hindari perpaduan warna yang menyulitkan pembacaan.
- **Navigasi Sederhana**: Alur navigasi harus intuitif dan tidak membingungkan. Kurangi jumlah klik yang diperlukan untuk mencapai fitur utama.
- **Elemen Interaktif yang Jelas**: Tombol dan tautan harus berukuran cukup besar agar mudah ditekan (touch-friendly) dan diberi label yang sangat jelas fungsinya. Hindari ikon tanpa label teks.
- **Bantuan & Pesan Kesalahan**: Pesan kesalahan (error) dan notifikasi sukses harus ditulis dengan bahasa yang sederhana, jelas, dan ditempatkan pada area yang mudah terlihat.

## 1. Teknologi & Library
- **Framework**: Vue.js 3 (Options API atau Composition API).
- **Styling**: Bootstrap 5 (CSS & JS via CDN atau NPM).
- **Icons**: Bootstrap Icons atau FontAwesome.
- **Form Validation**: Native HTML5 validation dikombinasikan dengan logika Vue.js.

## 2. Arsitektur Hak Akses (RBAC)
- **Role Detection**: Aplikasi akan mendeteksi `role` user dari data login (Account).
- **Conditional Rendering**: Elemen navigasi dan fitur akan ditampilkan/disembunyikan menggunakan direktif `v-if` berdasarkan role pengguna.
- **Protected Views**: Setiap role diarahkan ke halaman dashboard yang berbeda.

## 3. Desain Halaman per Role

### A. Dashboard Admin Daerah
- **Sidebar**: Link ke "Statistik Wilayah", "Daftar Sasana", "Registrasi Sasana Baru", dan "Manajemen Slidebar".
- **Main Content**:
  - **Statistik**: Card Bootstrap berisi jumlah sasana, peserta, dll.
  - **Tabel Sasana**: Menampilkan daftar sasana dengan fitur filter dan tombol edit.
  - **Form Registrasi**: Modal atau halaman terpisah untuk mendaftarkan sasana baru. Form ini **wajib** mencakup pembuatan akun untuk **Admin Sasana** secara bersamaan saat sasana baru didaftarkan, beserta validasi field wajib lainnya.
  - **Manajemen Slidebar**: Antarmuka untuk mengunggah dan mengelola gambar/foto pada slide bar (carousel) halaman utama, termasuk pengaturan teks pendamping.

### B. Dashboard Admin Sasana
- **Sidebar**: Link ke "Data Peserta", "Data Instruktur", "Data Pengurus", dan "Profil Sasana".
- **Main Content**:
  - **Manajemen Peserta**: Tabel responsif dengan fitur pencarian (NIK/Nama).
  - **Form Peserta**: Form detail untuk input data peserta termasuk riwayat kesehatan (Keterbatasan/Kendala).
  - **Form Instruktur/Pengurus**: Form dengan validasi format nomor HP dan ID Instruktur.
  - **Edit Profil Sasana**: Form untuk melengkapi dan memperbarui informasi detail sasana (seperti alamat lengkap, koordinat peta/map, dan profil deskriptif).

### C. Halaman Publik (Tanpa Login)
- **Landing Page (Beranda)**:
  - **Hero Section**: Memuat *Carousel* (slider/slidebar) foto dokumentasi kegiatan terapi Ling Tien Kung untuk memperkenalkan aktivitas sasana secara visual. Tata letak (layout) dirancang secara spesifik dengan gambar yang mendominasi dan **teks keterangan diletakkan secara jelas di sisi bawah** bersama gambar tersebut.
  - **Call to Action**: Terdapat tautan/tombol cepat menuju pencarian sasana terdekat atau halaman pendaftaran.
- **Menu Utama**: Daftar 10 Sasana Terdekat.
  - Ditampilkan berdasarkan deteksi lokasi pengguna.
  - **UI/UX**: Menggunakan elemen Card (kartu) yang menarik, menampilkan sekilas profil sasana beserta tombol/tautan langsung ke Google Maps.
- **Pencarian Lokasi Sasana**:
  - Pengguna dapat mencari sasana menggunakan filter: **Propinsi**, **Kabupaten**, dan **Kecamatan**.
  - **Hasil Pencarian**: Disajikan dalam format tabel yang jelas (mempertimbangkan ukuran font untuk usia 40-58 tahun), berisi Nama Sasana, Alamat Lengkap, dan Link/Tombol untuk mengecek lokasi via peta.

### D. Halaman Login & Registrasi
- **Halaman Login**:
  - Form input `Username` dan `Password`.
  - Tombol "Login" yang mencolok.
  - **Link Registrasi**: Terdapat tautan "Belum punya akun? Daftar di sini" yang mengarahkan ke halaman registrasi mandiri untuk peserta.
- **Halaman Registrasi Mandiri**:
  - Form pendaftaran untuk **Peserta** baru.
  - Memerlukan input data dasar sesuai spesifikasi model `Peserta` (Nama, NIK, No HP, dll).
  - **Pemilihan Sasana**: Calon peserta **wajib** memilih sasana tempat mereka mendaftar. Untuk kemudahan, fitur ini dilengkapi dengan pencarian langsung (searchable dropdown/autocomplete) berdasarkan nama sasana, atau calon peserta dapat mendaftar langsung melalui tombol registrasi yang tersedia di profil sasana pada Halaman Publik.
  - Validasi real-time untuk memastikan data unik (seperti NIK).

## 4. Komponen UI Standar

### Tabel Data
- Menggunakan class `.table .table-hover .table-striped` dari Bootstrap.
- Baris tabel responsif untuk tampilan mobile.

### Formulir & Validasi
- Menggunakan `.form-control` dan `.form-label` dari Bootstrap.
- **Validasi Visual**: Menggunakan class `.is-invalid` dan pesan `.invalid-feedback` saat input tidak sesuai kriteria.
- **Kriteria Validasi**:
  - NIK: Harus 16 digit angka.
  - No HP: Format nomor telepon Indonesia.
  - Field Wajib: Tidak boleh kosong sebelum tombol submit aktif.

## 5. Navigasi & Layout
- **Desain Responsif**: Seluruh antarmuka aplikasi **wajib** responsif dan menggunakan grid system Bootstrap agar tampilan menyesuaikan secara otomatis dengan berbagai ukuran layar pengguna (mobile, tablet, dan desktop).
- **Navbar Utama**: Menampilkan logo Eltekers, nama user yang login, dan tombol Logout. Pada layar kecil, navbar menggunakan menu hamburger (*collapse*).
- **Footer**: Informasi hak cipta dan versi aplikasi.
