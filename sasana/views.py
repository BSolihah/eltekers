from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import Account, Sasana, Peserta, Instruktur, PengurusSasana

def landing(request):
    return render(request, 'landing.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            if user.role == 'ADMIN_DAERAH':
                return redirect('dashboard_daerah')
            elif user.role == 'ADMIN_SASANA':
                return redirect('dashboard_sasana')
            else:
                return redirect('landing') # Untuk peserta/instruktur sementara
        else:
            from django.contrib import messages
            messages.error(request, "Username atau password salah.")
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Validasi NIK unik (sederhana)
            if Peserta.objects.filter(nik=data.get('nik')).exists():
                return JsonResponse({"error": "NIK sudah terdaftar."}, status=400)
            if Account.objects.filter(username=data.get('username')).exists():
                return JsonResponse({"error": "Username sudah digunakan."}, status=400)
            
            # Buat Account
            account = Account.objects.create_user(
                username=data.get('username'),
                password=data.get('password'),
                nama=data.get('nama'),
                email=data.get('email', ''),
                role='PESERTA'
            )
            
            # Buat Peserta
            sasana = Sasana.objects.get(id=data.get('sasana_id'))
            Peserta.objects.create(
                account=account,
                sasana=sasana,
                nik=data.get('nik'),
                no_hp=data.get('no_hp'),
                tanggal_lahir=data.get('tanggal_lahir'),
                berat_badan=data.get('berat_badan') or None,
                tinggi_badan=data.get('tinggi_badan') or None
            )
            return JsonResponse({"message": "Berhasil daftar"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def dashboard_daerah(request):
    if request.user.role != 'ADMIN_DAERAH':
        return redirect('landing')
    stats = {
        'total_sasana': Sasana.objects.count(),
        'total_peserta': Peserta.objects.count(),
        'total_instruktur': Instruktur.objects.count(),
        'total_pengurus': PengurusSasana.objects.count(),
    }
    return render(request, 'dashboard_daerah.html', {'stats': stats})

@login_required
def dashboard_sasana(request):
    if request.user.role != 'ADMIN_SASANA':
        return redirect('landing')
    # Default stats (ideally filtered by admin_sasana)
    stats = {
        'total_peserta': Peserta.objects.count(),
        'total_instruktur': Instruktur.objects.count(),
        'total_pengurus': PengurusSasana.objects.count(),
    }
    return render(request, 'dashboard_sasana.html', {'stats': stats})
