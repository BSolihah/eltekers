from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN_DAERAH', 'Admin Daerah'),
        ('ADMIN_SASANA', 'Admin Sasana'),
        ('PENGURUS_SASANA', 'Pengurus Sasana'),
        ('INSTRUKTUR', 'Instruktur'),
        ('PESERTA', 'Peserta'),
    )
    nama = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Sasana(models.Model):
    nama = models.CharField(max_length=255)
    admin_sasana = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='sasana_managed')
    propinsi = models.CharField(max_length=100)
    kabupaten = models.CharField(max_length=100)
    kecamatan = models.CharField(max_length=100)
    kelurahan_desa = models.CharField(max_length=100)
    map = models.CharField(max_length=255, help_text="Koordinat Google Maps")
    profil = models.ImageField(upload_to='sasana_profiles/', null=True, blank=True)

    def __str__(self):
        return self.nama

class AdminDaerah(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    daerah = models.CharField(max_length=255)

    def __str__(self):
        return f"Admin Daerah: {self.daerah}"

class AdminSasana(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    sasana = models.ForeignKey(Sasana, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin Sasana: {self.sasana.nama}"

class PengurusSasana(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    sasana = models.ForeignKey(Sasana, on_delete=models.CASCADE)
    jabatan = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.account.nama} - {self.jabatan}"

class Instruktur(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    sasana = models.ForeignKey(Sasana, on_delete=models.CASCADE)
    no_hp = models.CharField(max_length=20)
    sertifikat = models.CharField(max_length=255)
    id_instruktur = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Instruktur: {self.account.nama}"

class Peserta(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    sasana = models.ForeignKey(Sasana, on_delete=models.CASCADE)
    no_hp = models.CharField(max_length=20)
    tanggal_lahir = models.DateField()
    nik = models.CharField(max_length=16, unique=True)
    berat_badan = models.DecimalField(max_digits=5, decimal_places=2)
    tinggi_badan = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Peserta: {self.account.nama}"

class KeterbatasanFisik(models.Model):
    peserta = models.ForeignKey(Peserta, on_delete=models.CASCADE, related_name='keterbatasan')
    jenis_keterbatasan = models.CharField(max_length=255)

class KendalaKesehatan(models.Model):
    peserta = models.ForeignKey(Peserta, on_delete=models.CASCADE, related_name='kendala')
    jenis_penyakit = models.CharField(max_length=255)

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
