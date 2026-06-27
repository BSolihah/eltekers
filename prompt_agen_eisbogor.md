# Prompt Agen AI: Impor Data Excel ke Django (Eisbogor)

Gunakan prompt di bawah ini untuk membuat skrip data entry otomatis dari Excel ke sistem Django Eisbogor.

## Prompt Template

```text
Tolong buatkan saya sebuah skrip Python untuk melakukan data entry secara terprogram otomatis dari sebuah file Excel. 

Konteks Proyek:
Proyek saya menggunakan framework Django. Saya ingin memasukkan data ini secara langsung menggunakan Django ORM (atau melalui pemanggilan REST API jika Anda menyarankan pendekatan itu).

Detail File Excel:
- Nama file/path: [data_peserta.xlsx]
- Nama Sheet yang akan dibaca (jika ada): [Sheet1]
- Struktur Kolom Excel (Header): [No, Nama Lengkap, NIK, Alamat, Tanggal Lahir]

Target Database (Model Django):
- Nama Aplikasi Django: [sasana]
- Nama Model: [Peserta]
- Pemetaan (Mapping) dari Excel ke Model Django:
  - Kolom [Nama Lengkap] -> Field [nama]
  - Kolom [NIK] -> Field [nik]
  - Kolom [Alamat] -> Field [alamat]
  - Kolom [Tanggal Lahir] -> Field [tanggal_lahir] (format Excel: [DD/MM/YYYY])

Persyaratan Tambahan Skrip:
1. Gunakan library pandas atau openpyxl untuk membaca file Excel.
2. Implementasikan try-except untuk menangani error per baris (misalnya jika ada baris yang kosong atau format tanggal salah), sehingga jika satu baris gagal, proses baris berikutnya tetap berjalan.
3. Buatkan fitur skip duplicate (jangan masukkan data jika [NIK] sudah ada di database).
4. Tolong buat ini dalam bentuk Django Custom Management Command (agar saya bisa menjalankannya dengan python manage.py import_data_peserta), lengkap dengan struktur foldernya.
5. Berikan instruksi cara menginstal library yang dibutuhkan dan cara mengeksekusi command tersebut.
```
