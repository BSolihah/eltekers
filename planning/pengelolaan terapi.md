# Spesifikasi Aplikasi Terapi (App `terapi`)

Aplikasi `terapi` merupakan modul yang terpisah dari aplikasi `sasana` pada proyek Eltekers. Modul ini bertanggung jawab untuk mengelola seluruh aspek terkait terapi fisik, mulai dari manajemen referensi gerakan, penjadwalan, hingga evaluasi peserta dan pengelolaan testimoni.

---

## 1. Arsitektur & Teknologi

*   **Backend Framework:** Django
*   **Database:** PostgreSQL
*   **Frontend:** Vue.js (via CDN) dengan styling CSS (berbagi desain sistem / style CSS dengan aplikasi `sasana`).
*   **Komunikasi Data:** REST API menggunakan Django REST Framework (DRF) atau JSON endpoints konvensional Django.

---

## 2. Diagram Database (ERD)

Berikut adalah representasi Entity Relationship Diagram (ERD) dari model database yang dibutuhkan:

```mermaid
erDiagram
    GerakanAcuan ||--o{ EvaluasiGerakan : "dievaluasi_dalam"
    GerakanAcuan {
        int id PK
        string kategori (pilihan: membangkitkan semangat, cas aki, membangkitkan tenaga titik nol, pengendapan)
        string nama_gerakan
        string link_youtube
        text manfaat
        text fokus_gerakan
        text panduan_gerakan
        datetime created_at
    }

    Testimoni {
        int id PK
        int peserta_id FK "Relasi ke User/Peserta"
        string nama_peserta testimoni
        text teks 
        string video_url
        string foto_url
        boolean is_published
        datetime created_at
    }

    JadwalTerapiSasana ||--o{ TerapiPeserta : "mencakup"
    JadwalTerapiSasana {
        int id PK
        int sasana_id FK "Relasi ke App Sasana"
        int instruktur_id FK "Relasi ke User/Instruktur"
        string hari
        time jam_mulai
    }

    TerapiPeserta ||--o{ EvaluasiGerakan : "memiliki"
    TerapiPeserta {
        int id PK
        int jadwal_id FK
        int peserta_id FK "Relasi ke Peserta"
        string status_kehadiran
    }

    EvaluasiGerakan {
        int id PK
        int terapi_peserta_id FK
        int gerakan_acuan_id FK
        int instruktur_id FK
        string kesesuaian "tidak_mampu / belum_sesuai / sesuai "
        text catatan_instruktur
        datetime tanggal_evaluasi
    }
```

*Catatan: Model yang mengacu pada `Peserta`, `Instruktur`, dan `Sasana` diasumsikan merujuk ke tabel yang sudah ada atau dikelola melalui `auth.User` dan relasi ke model di app `sasana`.*

---

## 3. Dokumentasi Model Data (Django Models)

1.  **GerakanAcuan**: Menyimpan detail panduan setiap gerakan. Terdapat URL YouTube, rincian manfaat, fokus gerakan, dan panduan teks agar user mudah memahami instruksi.
2.  **Testimoni**: Berisi rekaman keberhasilan/kemajuan peserta. Dapat memuat teks, foto, dan link/file video.
3.  **JadwalTerapiSasana**: Mengatur hari dan jam operasional terapi di tiap titik sasana.
4.  **TerapiPeserta**: Pencatatan kehadiran terapi peserta 
5.  **EvaluasiGerakan**: Modul tempat Instruktur mencatat ketepatan gerakan peserta secara berkala.

---

## 4. Spesifikasi API (Backend)

API akan mengembalikan data dalam format JSON. Endpoints ini akan dipanggil menggunakan `axios` atau `fetch` oleh Vue.js di sisi frontend.

### A. Gerakan Acuan (Reference Movements)
*   `GET /api/terapi/gerakan/`
    *   **Deskripsi**: Menampilkan daftar gerakan acuan.
    *   **Query Params**: `?kategori=<id>` untuk filter kategori.
    *   **Akses**: User Terdaftar (Peserta, Instruktur, Admin).
*   `GET /api/terapi/gerakan/{id}/`
    *   **Deskripsi**: Detail gerakan acuan.
*   `POST /api/terapi/gerakan/`
    *   **Deskripsi**: Menambah gerakan acuan baru.
    *   **Akses**: Admin / Instruktur.
*   `PUT/PATCH /api/terapi/gerakan/{id}/`
    *   **Deskripsi**: Mengedit data gerakan acuan.
*   `DELETE /api/terapi/gerakan/{id}/`
    *   **Deskripsi**: Menghapus data gerakan acuan.

### B. Testimoni
*   `GET /api/terapi/testimoni/`
    *   **Deskripsi**: Menampilkan daftar testimoni untuk Landing Page.
    *   **Akses**: Public (Guest/Semua Orang).
*   `POST /api/terapi/testimoni/`
    *   **Deskripsi**: Membuat testimoni.
    *   **Akses**: Admin / Sistem.
*   `PUT/PATCH /api/terapi/testimoni/{id}/`
    *   **Deskripsi**: Update testimoni (misal: set `is_published = True`).
*   `DELETE /api/terapi/testimoni/{id}/`
    *   **Deskripsi**: Menghapus testimoni.

### C. Jadwal Terapi Sasana
*   `GET /api/terapi/jadwal/?sasana_id={id}`
    *   **Deskripsi**: Melihat jadwal operasional.
*   `POST /api/terapi/jadwal/`
    *   **Deskripsi**: Menambah jadwal untuk suatu sasana.
*   `PUT/PATCH /api/terapi/jadwal/{id}/`
*   `DELETE /api/terapi/jadwal/{id}/`

### D. Terapi Peserta (Sesi/Kehadiran)
*   `GET /api/terapi/sesi-peserta/`
    *   **Deskripsi**: Menampilkan daftar terapi untuk peserta tertentu, atau peserta di jadwal tertentu.
*   `POST /api/terapi/sesi-peserta/`
    *   **Deskripsi**: Mendaftarkan peserta ke sesi terapi dan mencatat kehadirannya.
*   `PUT/PATCH /api/terapi/sesi-peserta/{id}/`
*   `DELETE /api/terapi/sesi-peserta/{id}/`

### E. Evaluasi Gerakan
*   `GET /api/terapi/evaluasi/?peserta_id={id}`
    *   **Deskripsi**: Melihat rekam jejak evaluasi gerakan untuk evaluasi performa terapi peserta.
*   `POST /api/terapi/evaluasi/`
    *   **Deskripsi**: Form submission oleh Instruktur mengenai hasil evaluasi (Skor dan Catatan).
*   `PUT/PATCH /api/terapi/evaluasi/{id}/`
*   `DELETE /api/terapi/evaluasi/{id}/`

---

## 5. Spesifikasi Frontend (Vue.js CDN)

Frontend dibuat secara terpisah pada level template menggunakan CDN Vue.js untuk reaktivitas. **Aplikasi ini Wajib menggunakan CSS layout yang sama dengan aplikasi `sasana` untuk menjaga identitas visual (UI/UX) Eltekers.**

### Modul Antarmuka (UI):

1.  **Halaman Katalog Gerakan (Untuk Peserta Terdaftar)**
    *   **Fitur Vue**: Menggunakan `v-for` untuk list grid/cards gerakan acuan, dan input filter `v-model` (pencarian teks dan kategori).
    *   **Tampilan**: Menampilkan thumbnail video Youtube, judul, fokus, dan tombol "Lihat Detail" yang membuka pop-up Modal atau Halaman baru berisi panduan lengkap.

2.  **Manajemen Gerakan Acuan (Admin/Instruktur)**
    *   Tabel CRUD Gerakan yang dilengkapi tombol "Tambah", "Edit", "Hapus".
    *   Terdapat Form (via Vue Component/Modal) untuk menginput link YouTube dan secara otomatis merender iFrame preview videonya.

3.  **Halaman Testimoni (Guest)**
    *   Dibuat publik.
    *   Desain berupa slider/carousel berisi foto/video testimoni dilengkapi teks ulasan keberhasilan terapi.

4.  **Manajemen Jadwal Terapi (Admin Sasana)**
    *   Kalender atau daftar hari yang menampilkan jam sesi dan instruktur yang bertugas. Tersedia input CRUD.

5.  **Dashboard Evaluasi Instruktur**
    *   Halaman interaktif bagi Instruktur yang menampilkan *List Kehadiran Peserta* di satu jadwal/hari.
    *   Saat nama peserta di-klik, muncul **Panel Evaluasi** berisi daftar gerakan yang harus dievaluasi
    *   Instruktur bisa langsung memberikan keterangan kesesuaian gerakan dan mengisi catatan langsung.
    
---

## 6. Alur Pengerjaan (Langkah Implementasi)

1.  **Inisialisasi Backend**
    *   Membuat aplikasi Django baru dengan `python manage.py startapp terapi` dan meregistrasikannya ke `settings.py`.
    *   Mendefinisikan skema pada `terapi/models.py`.
    *   Menjalankan `makemigrations` dan `migrate`.
2.  **Pembuatan Layer API**
    *   Membuat file `serializers.py`.
    *   Membuat controller di `api_views.py` (DRF viewsets / custom JsonResponse).
    *   Setup routing di `urls.py`.
3.  **Pembangunan Antarmuka Vue (Frontend)**
    *   Menyiapkan direktori `templates/terapi/` dan base file HTML yang extend layout CSS Sasana.
    *   Memisahkan *logic* JavaScript Vue di folder `static/terapi/js/`.
    *   Menghubungkan `axios` untuk melakukan request REST API dari halaman-halaman tersebut.
4.  **Pengujian dan Integrasi**
    *   Mendemonstrasikan fungsi evaluasi (termasuk validasi form).
    *   Memastikan UI responsif dan styling CSS selaras 100% dengan modul sasana.
