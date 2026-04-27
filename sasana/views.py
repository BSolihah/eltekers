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
            if getattr(user, 'force_password_change', False):
                return redirect('change_password')
            
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

@login_required
def change_password_view(request):
    if request.method == 'POST':
        p1 = request.POST.get('new_password')
        p2 = request.POST.get('confirm_password')
        from django.contrib import messages
        if not p1 or not p2:
            messages.error(request, "Password tidak boleh kosong.")
        elif p1 != p2:
            messages.error(request, "Password dan Konfirmasi Password tidak cocok.")
        else:
            user = request.user
            user.set_password(p1)
            user.force_password_change = False
            user.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            messages.success(request, "Password berhasil diubah. Selamat datang!")
            if user.role == 'ADMIN_DAERAH':
                return redirect('dashboard_daerah')
            elif user.role == 'ADMIN_SASANA':
                return redirect('dashboard_sasana')
            else:
                return redirect('landing')
    return render(request, 'change_password.html')

def forgot_password_view(request):
    return render(request, 'forgot_password.html')

def register_view(request):
    if request.method == 'POST':
        try:
            from django.db import transaction
            data = json.loads(request.body)
            # Validasi NIK unik (sederhana)
            if Peserta.objects.filter(nik=data.get('nik')).exists():
                return JsonResponse({"error": "NIK sudah terdaftar."}, status=400)
            if Account.objects.filter(username=data.get('username')).exists():
                return JsonResponse({"error": "Username sudah digunakan."}, status=400)
            
            with transaction.atomic():
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
                
                berat_badan = data.get('berat_badan')
                tinggi_badan = data.get('tinggi_badan')
                
                Peserta.objects.create(
                    account=account,
                    sasana=sasana,
                    nik=data.get('nik'),
                    no_hp=data.get('no_hp'),
                    tanggal_lahir=data.get('tanggal_lahir'),
                    berat_badan=berat_badan if berat_badan not in [None, ''] else 0,
                    tinggi_badan=tinggi_badan if tinggi_badan not in [None, ''] else 0
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
    
    from django.core.cache import cache
    stats = cache.get('daerah_stats')
    if not stats:
        stats = {
            'total_sasana': Sasana.objects.count(),
            'total_peserta': Peserta.objects.count(),
            'total_instruktur': Instruktur.objects.count(),
            'total_pengurus': PengurusSasana.objects.count(),
        }
        cache.set('daerah_stats', stats, 300) # Cache selama 5 menit
    return render(request, 'dashboard_daerah.html', {'stats': stats})

@login_required
def dashboard_sasana(request):
    if request.user.role != 'ADMIN_SASANA':
        return redirect('landing')
    
    # Ambil sasana yang dikelola admin ini
    try:
        sasana = request.user.adminsasana.sasana
    except Exception:
        # Jika profil admin sasana belum lengkap
        return render(request, 'dashboard_sasana.html', {
            'stats': {'total_peserta': 0, 'total_instruktur': 0, 'total_pengurus': 0},
            'error': 'Profil Admin Sasana belum terhubung dengan Sasana manapun.'
        })

    from django.core.cache import cache
    cache_key = f'sasana_stats_{sasana.id}'
    stats = cache.get(cache_key)
    if not stats:
        stats = {
            'total_peserta': Peserta.objects.filter(sasana=sasana).count(),
            'total_instruktur': Instruktur.objects.filter(sasana=sasana).count(),
            'total_pengurus': PengurusSasana.objects.filter(sasana=sasana).count(),
        }
        cache.set(cache_key, stats, 300)

    return render(request, 'dashboard_sasana.html', {
        'stats': stats,
        'sasana': sasana
    })
