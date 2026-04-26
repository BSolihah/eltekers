# Laporan Unit Testing - EIS Bogor

Laporan ini mendokumentasikan hasil pengujian unit (unit testing) yang dilakukan pada sistem EIS Bogor.

---

## Ringkasan Eksekusi
*   **Tanggal Pengujian**: 25 April 2026
*   **Total Test Case**: 8
*   **Status**: ✅ LULUS (ALL PASSED)
*   **Durasi**: 1.163s

---

## Detail Pengujian

### 1. SasanaModelTest
*   `test_sasana_creation`: Memastikan Sasana berhasil dibuat dan terhubung ke Admin Sasana dengan benar. **(PASSED)**
*   `test_account_role`: Memastikan role akun (ADMIN_SASANA) tersimpan dengan benar. **(PASSED)**
*   `test_cascade_delete_sasana`: Memastikan penghapusan Sasana otomatis menghapus Peserta terkait (Cascade Delete). **(PASSED)**

### 2. PesertaModelTest
*   `test_peserta_unique_nik`: Memastikan sistem menolak pendaftaran NIK yang duplikat (Unique Constraint). **(PASSED)**

### 3. SasanaAPITest
*   `test_get_sasana_list`: Memastikan API List Sasana mengembalikan data yang benar. **(PASSED)**
*   `test_search_sasana_by_name`: Memastikan fitur pencarian sasana berdasarkan nama berfungsi di level API. **(PASSED)**

### 4. PesertaAPITest
*   `test_search_peserta_by_nik`: Memastikan fitur pencarian peserta berdasarkan NIK berfungsi di level API. **(PASSED)**
*   `test_search_peserta_by_name`: Memastikan fitur pencarian peserta berdasarkan nama (via Account) berfungsi di level API. **(PASSED)**

---

## Log Output Terminal
```text
Found 8 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 1.163s

OK
Destroying test database for alias 'default'...
```

---
**Kesimpulan**: Seluruh fitur inti (Model dan API) telah lulus uji validasi dan siap untuk digunakan di lingkungan produksi.
