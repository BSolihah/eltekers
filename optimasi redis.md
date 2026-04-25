# Dokumentasi Optimasi Redis - EIS Bogor

Dokumen ini merinci implementasi dan optimasi sistem caching menggunakan Redis pada aplikasi EIS Bogor untuk meningkatkan performa di lingkungan produksi.

---

## 1. Arsitektur Caching
Sistem menggunakan **Redis** sebagai backend tunggal untuk dua fungsi kritis:
*   **Default Cache**: Menyimpan hasil kalkulasi statistik dan hasil query API wilayah yang jarang berubah.
*   **Session Storage**: Menggantikan database sebagai penyimpan sesi login pengguna untuk mempercepat proses autentikasi pada setiap request.

---

## 2. Fitur Optimasi Lanjutan

### A. Kompresi Data (Zlib Compression)
Seluruh data yang disimpan di Redis dikompresi menggunakan algoritma **Zlib**.
*   **Tujuan**: Mengurangi penggunaan memori RAM di server Redis hingga 40-60%.
*   **Dampak**: Mempercepat transfer data antara server Django dan Redis (throughput lebih tinggi).

### B. Invalidation Otomatis (Django Signals)
Sistem tidak lagi menghapus cache secara manual di dalam View. Sebagai gantinya, digunakan **Django Signals** (`sasana/signals.py`).
*   **Mekanisme**: Setiap kali ada operasi `post_save` atau `post_delete` pada model Peserta, Instruktur, atau Pengurus, sinyal akan memicu penghapusan cache terkait secara otomatis.
*   **Keuntungan**: Menjamin konsistensi data (statistik selalu akurat) dan menjaga kode program tetap bersih (*DRY - Don't Repeat Yourself*).

### C. Ketahanan Sistem (Fail-Silently)
Konfigurasi `IGNORE_EXCEPTIONS: True` diterapkan pada pengaturan cache.
*   **Manfaat**: Jika server Redis mengalami gangguan atau mati, aplikasi tidak akan berhenti (crash). Django akan otomatis beralih ke database utama tanpa mengganggu pengalaman pengguna.

### D. Isolasi Namespace (Key Prefix)
Menggunakan awalan `eis_bogor` untuk seluruh kunci cache.
*   **Manfaat**: Mencegah tabrakan data (*key collision*) jika satu server Redis digunakan oleh beberapa aplikasi berbeda.

---

## 3. Titik Optimasi Utama

1.  **Dashboard Statistics**: Kecepatan muat halaman meningkat karena statistik tidak lagi dihitung ulang dari database setiap kali halaman dibuka (Cached 5 menit).
2.  **API Proxy Wilayah**: Dropdown lokasi (Provinsi/Kota) menjadi instan karena data eksternal disimpan di cache lokal (Cached 24 jam).
3.  **Query Optimization**: Penggunaan `select_related` pada ViewSet memastikan data relasional (Account & Sasana) diambil dalam satu query JOIN yang efisien.

---
**Kesimpulan**: Implementasi Redis ini dirancang untuk skalabilitas tinggi, memastikan aplikasi tetap responsif meskipun jumlah pengguna dan data terus bertambah.
