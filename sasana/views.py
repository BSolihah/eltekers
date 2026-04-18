from django.shortcuts import render
from .models import Sasana, Peserta, Instruktur, PengurusSasana

def index(request):
    return render(request, 'base.html')

def dashboard_daerah(request):
    # Logika statistik sederhana untuk dashboard daerah
    stats = {
        'total_sasana': Sasana.objects.count(),
        'total_peserta': Peserta.objects.count(),
        'total_instruktur': Instruktur.objects.count(),
        'total_pengurus': PengurusSasana.objects.count(),
    }
    return render(request, 'dashboard_daerah.html', {'stats': stats})

def dashboard_sasana(request):
    # Logika statistik untuk satu sasana (contoh filter bisa ditambahkan nanti)
    stats = {
        'total_peserta': Peserta.objects.count(),
        'total_instruktur': Instruktur.objects.count(),
        'total_pengurus': PengurusSasana.objects.count(),
    }
    return render(request, 'dashboard_sasana.html', {'stats': stats})
