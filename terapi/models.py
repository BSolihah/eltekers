from django.db import models
from sasana.models import Sasana, Peserta, Instruktur

class GerakanAcuan(models.Model):
    KATEGORI_CHOICES = [
        ('membangkitkan semangat', 'Membangkitkan Semangat'),
        ('cas aki', 'Cas Aki'),
        ('membangkitkan energi titik nol', 'Membangkitkan Energi Titik Nol'),
        ('pengendapan', 'Pengendapan'),
    ]
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    nama_gerakan = models.CharField(max_length=255)
    link_youtube = models.URLField(max_length=500)
    manfaat = models.TextField()
    fokus_gerakan = models.TextField()
    panduan_gerakan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_gerakan} ({self.get_kategori_display()})"

class Testimoni(models.Model):
    peserta = models.ForeignKey(Peserta, on_delete=models.CASCADE, related_name='testimoni')
    nama_peserta = models.CharField(max_length=255)
    teks = models.TextField()
    video_url = models.URLField(max_length=500, blank=True, null=True)
    foto_url = models.ImageField(upload_to='testimoni/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimoni dari {self.nama_peserta}"

class JadwalTerapiSasana(models.Model):
    HARI_CHOICES = [
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
        ('Sabtu', 'Sabtu'),
        ('Minggu', 'Minggu'),
    ]
    sasana = models.ForeignKey(Sasana, on_delete=models.CASCADE, related_name='jadwal_terapi')
    instruktur = models.ForeignKey(Instruktur, on_delete=models.CASCADE, related_name='jadwal_terapi')
    hari = models.CharField(max_length=50, choices=HARI_CHOICES)
    jam_mulai = models.TimeField()

    def __str__(self):
        return f"{self.sasana.nama} - {self.hari} {self.jam_mulai}"

class TerapiPeserta(models.Model):
    STATUS_KEHADIRAN_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Tidak Hadir', 'Tidak Hadir'),
        ('Izin', 'Izin'),
    ]
    jadwal = models.ForeignKey(JadwalTerapiSasana, on_delete=models.CASCADE, related_name='sesi_peserta')
    peserta = models.ForeignKey(Peserta, on_delete=models.CASCADE, related_name='sesi_terapi')
    status_kehadiran = models.CharField(max_length=50, choices=STATUS_KEHADIRAN_CHOICES)

    def __str__(self):
        return f"{self.peserta.account.nama} - {self.jadwal}"

class EvaluasiGerakan(models.Model):
    KESESUAIAN_CHOICES = [
        ('tidak bisa', 'Tidak Bisa'),
        ('kurang sesuai', 'Kurang Sesuai'),
        ('bisa', 'Bisa'),
    ]
    terapi_peserta = models.ForeignKey(TerapiPeserta, on_delete=models.CASCADE, related_name='evaluasi')
    gerakan_acuan = models.ForeignKey(GerakanAcuan, on_delete=models.CASCADE)
    instruktur = models.ForeignKey(Instruktur, on_delete=models.CASCADE)
    kesesuaian = models.CharField(max_length=20, choices=KESESUAIAN_CHOICES)
    catatan_instruktur = models.TextField(blank=True, null=True)
    tanggal_evaluasi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluasi {self.terapi_peserta.peserta.account.nama} - {self.gerakan_acuan.nama_gerakan}"
