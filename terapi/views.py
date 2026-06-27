from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Halaman Publik
def testimoni_katalog_view(request):
    return render(request, 'terapi/testimoni_list.html')

# Halaman User Terdaftar
@login_required
def gerakan_katalog_view(request):
    return render(request, 'terapi/gerakan_list.html')

# Manajemen oleh Admin/Instruktur
@login_required
def gerakan_manage_view(request):
    return render(request, 'terapi/gerakan_manage.html')

@login_required
def testimoni_manage_view(request):
    return render(request, 'terapi/testimoni_manage.html')

@login_required
def jadwal_manage_view(request):
    return render(request, 'terapi/jadwal_manage.html')

@login_required
def evaluasi_peserta_view(request):
    return render(request, 'terapi/evaluasi_peserta.html')
