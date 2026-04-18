# Spesifikasi Sistem Manajemen Sasana Eltekers

Dokumen ini berisi spesifikasi model, view, dan fitur yang akan diimplementasikan dalam aplikasi web Sistem Basis Data Eltekers.

## 1. Data Models (Django Models)

- **Account**: Base model untuk semua pengguna.
  - Fields: `username`, `password`, `nama`, `email`, `role`.
- **AdminDaerah**: Pengelola tingkat wilayah.
  - Fields: `account` (FK to Account), `daerah`.
- **AdminSasana**: Administrator tingkat sasana.
  - Fields: `account` (FK to Account), `sasana` (FK to Sasana).
- **Sasana**: Unit terapi lokal.
  - Fields: `nama`, `admin_sasana` (FK to Account), `propinsi`, `kabupaten`, `kecamatan`, `kelurahan_desa`, `map` (koordinat), `profil`.
- **PengurusSasana**: Tim pengelola sasana.
  - Fields: `account` (FK to Account), `sasana` (FK to Sasana), `jabatan`, `no_hp`.
- **Instruktur**: Tenaga pelatih.
  - Fields: `account` (FK to Account), `sasana` (FK to Sasana), `no_hp`, `sertifikat`, `id_instruktur`.
- **Peserta**: Anggota terapi.
  - Fields: `account` (FK to Account), `sasana` (FK to Sasana), `no_hp`, `tanggal_lahir`, `nik`, `berat_badan`, `tinggi_badan`.
- **KeterbatasanFisik**: Data kondisi fisik peserta.
  - Fields: `peserta` (FK to Peserta), `jenis_keterbatasan`.
- **KendalaKesehatan**: Data riwayat penyakit peserta.
  - Fields: `peserta` (FK to Peserta), `jenis_penyakit`.

## 2. Views & Endpoints (Django Rest Framework)

Seluruh view diimplementasikan menggunakan pendekatan **REST API** menggunakan Django Rest Framework.

### Fitur Admin Daerah:
- **Pendaftaran Sasana**: Mendaftarkan `nama` sasana dan `admin_sasana`.
- **Manajemen Sasana**: Edit dan View detail data seluruh sasana di wilayahnya.

### Fitur Admin Sasana:
- **Pendaftaran & Manajemen Peserta**: Create, Edit, View detail data peserta.
- **Pendaftaran & Manajemen Instruktur**: Create, Edit, View detail data instruktur.
- **Pendaftaran & Manajemen Pengurus Sasana**: Create, Edit, View detail data pengurus.
- **Manajemen Kesehatan**: Kelola data `KeterbatasanFisik` dan `KendalaKesehatan` peserta.
- **Edit Sasana**: Melengkapi profil dan lokasi sasana.

### Fitur Publik/Umum:
- **Daftar Sasana**: Menampilkan sasana berdasarkan filter `propinsi`, `kabupaten`, `kecamatan`, `kelurahan_desa`.

## 3. Fitur Tambahan & Keamanan
- **Hak Akses**: Implementasi Role-Based Access Control (RBAC) menggunakan `role`.
- **Pencarian Peserta**: Berdasarkan `NIK` atau `Nama`.
- **Pencarian Sasana**: Berdasarkan lokasi/peta (`map`).

## 4. Dashboard
- **Dashboard Pengurus Daerah**:
  - Total Sasana.
  - Sebaran Sasana di daerah.
  - Total Peserta, Instruktur, dan Pengurus Sasana di wilayah terkait.
- **Dashboard Pengurus Sasana**:
  - Total Peserta, Instruktur, dan Pengurus Sasana di sasana tersebut.

## 5. Catatan Revisi & Perbaikan
- **UI Dashboard Sasana**: Perbaikan tampilan tabel peserta agar header tidak keluar dari container/box (overflow issue).
