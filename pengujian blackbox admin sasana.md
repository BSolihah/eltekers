# Laporan Pengujian Blackbox: Alur Admin Sasana - EIS Bogor

Laporan ini mendokumentasikan hasil pengujian antarmuka (Frontend) untuk peran Admin Sasana, mulai dari halaman depan hingga proses keluar dari sistem.

---

## Ringkasan Pengujian
*   **Tanggal Pengujian**: 25 April 2026
*   **User Test**: `admin_sasana_baru`
*   **Browser**: Chrome (Headless via Playwright)
*   **Status Keseluruhan**: ✅ **LULUS (100% Passed)**

---

## Tabel Hasil Pengujian

| No | Langkah Pengujian | Hasil yang Diharapkan | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Akses Landing Page (`/`) | Halaman utama berhasil dimuat | ✅ **PASSED** | Konten hero dan navbar muncul dengan benar. |
| 2 | Navigasi ke Halaman Login | Redirect ke `/login/` berhasil | ✅ **PASSED** | Form login muncul dengan field Username dan Password. |
| 3 | Login (User: `admin_sasana_baru`) | Berhasil autentikasi | ✅ **PASSED** | Autentikasi sukses dengan kredensial yang valid. |
| 4 | Verifikasi Redirection Dashboard | Dialihkan ke `/dashboard/sasana/` | ✅ **PASSED** | Redirection otomatis setelah login berhasil. |
| 5 | Cek Kartu Statistik | Statistik Peserta, Instruktur, Pengurus terlihat | ✅ **PASSED** | Ketiga kartu statistik muncul di bagian atas dashboard. |
| 6 | Cek Tabel Peserta | Tabel "Daftar Peserta Sasana" terlihat | ✅ **PASSED** | Tabel berhasil dimuat dan menampilkan struktur data. |
| 7 | Logout | Berhasil keluar dari sistem | ✅ **PASSED** | Sesi berakhir dan menu profil tertutup. |
| 8 | Verifikasi Redirection Logout | Dialihkan kembali ke Landing Page | ✅ **PASSED** | Kembali ke halaman utama (guest mode). |

---

## Observasi Visual
*   **Kecepatan**: Halaman dashboard dimuat dengan cepat setelah login (< 1 detik).
*   **Responsivitas**: Elemen tabel dan kartu statistik menyesuaikan lebar layar dengan baik.
*   **Navigasi**: Menu dropdown profil berfungsi dengan lancar untuk akses logout.

---

## Kesimpulan
Berdasarkan pengujian blackbox yang dilakukan, alur kerja frontend untuk Admin Sasana telah memenuhi standar fungsionalitas. Tidak ditemukan *dead link* atau kegagalan navigasi pada jalur kritis (Critical Path) aplikasi.
