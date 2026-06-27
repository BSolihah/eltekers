# Spesifikasi Aplikasi Ekstensi Eltekers: Presensi & Evaluasi Gerakan

Dokumen ini berisi spesifikasi teknis dan panduan implementasi untuk membuat aplikasi web terpisah (ekstensi) yang berfungsi untuk melakukan perekaman kehadiran (QR Code) dan evaluasi gerakan terapi (Computer Vision). Spesifikasi ini dirancang sedetail mungkin agar dapat diimplementasikan lapis demi lapis oleh model AI (seperti Gemini Flash) untuk memastikan hasil kode akurat dan minim perbaikan.

## 1. Arsitektur & Teknologi Utama
- **Frontend (Aplikasi Ekstensi):** Vue 3 dengan Vite (Composition API, `<script setup>`).
- **Styling:** Bootstrap 5 (mengikuti standar UI aplikasi Eltekers yang sudah ada).
- **HTTP Client:** Axios (untuk komunikasi dengan API Django).
- **Scanner Kehadiran:** `html5-qrcode`.
- **Evaluasi Gerakan:** `@mediapipe/pose` dan `@mediapipe/camera_utils` (berjalan sepenuhnya di browser klien), membandingkan gerakan peserta dengan data **gerakan acuan** (video/sensor).
- **Justifikasi Instruktur:** Antarmuka khusus bagi instruktur untuk meninjau dan memvalidasi hasil evaluasi otomatis.
- **Integrasi Backend:** Django REST Framework (DRF) dengan `djangorestframework-simplejwt` untuk autentikasi dan `django-cors-headers` untuk mengizinkan akses beda domain.

## 2. Kebutuhan Endpoint API (Sisi Backend Django)
Sebelum membangun frontend, AI harus mengimplementasikan API berikut di aplikasi Eltekers:

1.  **Autentikasi (JWT):**
    -   `POST /api/token/` (Mendapatkan token akses login pengguna).
2.  **Presensi / Kehadiran:**
    -   `POST /api/kehadiran/`
    -   *Payload yang diharapkan:* `{"peserta_id": 1, "sasana_id": 2, "tanggal": "2026-06-27"}`
    -   *Response:* Status 201 (Berhasil).
3.  **Gerakan Acuan (Reference Data):**
    -   `GET /api/gerakan-acuan/` (Mendapatkan data titik sensor atau video gerakan acuan).
    -   `POST /api/gerakan-acuan/` (Menyimpan gerakan acuan baru oleh instruktur).
4.  **Evaluasi Gerakan (Sistem Otomatis):**
    -   `POST /api/evaluasi-gerakan/`
    -   *Payload yang diharapkan:* `{"peserta_id": 1, "acuan_id": 5, "skor_otomatis": 85, "data_sensor": [...]}`
    -   *Response:* Status 201 (Penyimpanan berhasil, status "menunggu_justifikasi").
5.  **Justifikasi Evaluasi (Instruktur):**
    -   `POST /api/evaluasi-gerakan/{id}/justifikasi/`
    -   *Payload yang diharapkan:* `{"skor_akhir": 90, "catatan_instruktur": "Gerakan kaki sudah bagus", "status": "disetujui"}`
    -   *Response:* Status 200 (Berhasil diperbarui).

## 3. Struktur Proyek Frontend (Vue 3 Vite)
Berikan referensi struktur ini agar AI mengetahui peletakan file yang tepat:
```text
src/
├── assets/
├── components/
│   ├── ScannerQR.vue         # Komponen untuk memindai QR Code
│   ├── PoseEvaluator.vue     # Komponen kamera untuk MediaPipe Pose
│   └── Navbar.vue            # Navigasi utama Bootstrap
├── views/
│   ├── Login.vue             # Halaman login (mendapatkan JWT)
│   ├── Presensi.vue          # Halaman presensi (menampilkan ScannerQR)
│   ├── KelolaAcuan.vue       # Halaman bagi instruktur merekam/mengunggah gerakan acuan
│   ├── Evaluasi.vue          # Halaman evaluasi (membandingkan gerakan dengan acuan)
│   └── Justifikasi.vue       # Halaman bagi instruktur memvalidasi hasil evaluasi otomatis
├── router/
│   └── index.js              # Routing halaman (Vue Router)
├── stores/
│   └── auth.js               # Pinia store untuk menyimpan JWT dan status user
├── App.vue
└── main.js
```

## 4. Instruksi Implementasi Bertahap (Prompt Guidelines untuk AI)
Gunakan prompt berikut secara bertahap dan berurutan saat berinteraksi dengan AI untuk mengimplementasikan kode. Berikan satu prompt di setiap percakapan.

### Tahap 1: Persiapan Backend Django (API & CORS)
**Prompt untuk AI:**
> "Saya memiliki proyek Django bernama `eisbogor`. Tolong berikan panduan dan kode untuk:
> 1. Menginstal dan mengonfigurasi `django-cors-headers` di `settings.py` untuk mengizinkan domain `http://localhost:5173`.
> 2. Menginstal dan mengonfigurasi `djangorestframework-simplejwt`.
> 3. Membuat viewset/endpoint DRF untuk `Kehadiran`, `GerakanAcuan`, dan `EvaluasiGerakan` (termasuk fungsi kustom `@action` untuk justifikasi instruktur). Berikan contoh model Django untuk masing-masing."

### Tahap 2: Inisialisasi Proyek Vue 3 & Routing
**Prompt untuk AI:**
> "Buat proyek Vue 3 menggunakan Vite. Berikan daftar perintah untuk instalasi awal.
> Kemudian, berikan contoh isi `package.json` yang berisi dependensi: `vue-router`, `pinia`, `axios`, `html5-qrcode`, `@mediapipe/pose`, `@mediapipe/camera_utils`, dan `bootstrap`.
> Setelah itu, buatkan struktur file `src/router/index.js` dengan rute: `/login`, `/presensi`, `/kelola-acuan`, `/evaluasi`, dan `/justifikasi`."

### Tahap 3: Pembuatan Komponen Presensi (QR Code)
**Prompt untuk AI:**
> "Buat komponen `ScannerQR.vue` menggunakan Vue 3 Composition API (`<script setup>`).
> Gunakan library `html5-qrcode` untuk mengakses kamera perangkat dan membaca QR Code. 
> Saat QR Code terbaca dengan sukses, ambil teks datanya, bunyikan suara beep kecil (opsional), lalu gunakan Axios untuk mengirim HTTP POST request ke `http://localhost:8000/api/kehadiran/`. Pastikan Anda menyertakan JWT token di header Authorization Bearer."

### Tahap 4: Pembuatan Komponen Evaluasi Gerakan (MediaPipe)
**Prompt untuk AI:**
> "Buat komponen `PoseEvaluator.vue` menggunakan Vue 3 Composition API.
> 1. Buat mekanisme *fetch* (GET) dengan Axios untuk mengambil data titik sensor dari `GerakanAcuan` sebelum evaluasi dimulai.
> 2. Pasang tag `<video>` untuk menampilkan tangkapan kamera dan `<canvas>` transparan di atasnya untuk menggambar *skeleton* titik tubuh (landmarks).
> 3. Integrasikan inisialisasi `@mediapipe/pose` dan mulailah membaca *frame* kamera menggunakan `@mediapipe/camera_utils`.
> 4. Saat pose terdeteksi di event `onResults`, ekstrak array `results.poseLandmarks` dan bandingkan (komparasi) secara *real-time* dengan data sensor dari Gerakan Acuan (menggunakan algoritma komparasi titik sendi/waktu).
> 5. Buatkan tombol 'Selesai & Simpan' yang apabila diklik akan mengirim skor evaluasi hasil komparasi otomatis tersebut ke `http://localhost:8000/api/evaluasi-gerakan/` menggunakan Axios dengan status default 'menunggu justifikasi'."

### Tahap 5: Pembuatan Komponen Kelola Acuan & Justifikasi Instruktur
**Prompt untuk AI:**
> "Buat dua komponen baru menggunakan Vue 3 Composition API:
> 1. `KelolaAcuan.vue`: Halaman yang menggunakan MediaPipe untuk merekam gerakan instruktur secara ideal dan menyimpannya sebagai JSON (data sensor titik sendi tiap *frame*) via `POST /api/gerakan-acuan/`.
> 2. `JustifikasiInstruktur.vue`: Halaman yang mengambil daftar evaluasi peserta yang berstatus 'menunggu justifikasi', menampilkannya dalam tabel, dan menyediakan form bagi instruktur untuk memasukkan skor akhir (manual override) beserta catatan. Gunakan Axios untuk mengirim `POST /api/evaluasi-gerakan/{id}/justifikasi/`."

