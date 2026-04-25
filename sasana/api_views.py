from rest_framework import viewsets, filters, status
from django.db import transaction
from .models import (
    Account, Sasana, AdminDaerah, AdminSasana, 
    PengurusSasana, Instruktur, Peserta, 
    KeterbatasanFisik, KendalaKesehatan, CarouselImage
)
from .serializers import (
    AccountSerializer, SasanaSerializer, AdminDaerahSerializer, 
    AdminSasanaSerializer, PengurusSasanaSerializer, 
    InstrukturSerializer, PesertaSerializer,
    KeterbatasanFisikSerializer, KendalaKesehatanSerializer,
    CarouselImageSerializer
)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
import math

class SasanaViewSet(viewsets.ModelViewSet):
    queryset = Sasana.objects.all()
    serializer_class = SasanaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'propinsi', 'kabupaten', 'kecamatan', 'kelurahan_desa', 'map']

    def create(self, request, *args, **kwargs):
        data = request.data
        admin_username = data.get('admin_username')
        admin_password = 'sasana123'
        admin_nama = data.get('admin_nama')
        admin_email = data.get('admin_email', '')

        if not all([admin_username, admin_nama]):
            return Response({"error": "Data admin sasana (username, nama) wajib diisi untuk registrasi sasana baru."}, status=status.HTTP_400_BAD_REQUEST)

        if Account.objects.filter(username=admin_username).exists():
            return Response({"error": "Username admin sudah digunakan."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Create Account for Admin Sasana
                admin_account = Account.objects.create_user(
                    username=admin_username,
                    password=admin_password,
                    nama=admin_nama,
                    email=admin_email,
                    role='ADMIN_SASANA',
                    force_password_change=True
                )

                # 2. Create Sasana and assign admin
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                sasana = serializer.save(admin_sasana=admin_account)

                # 3. Create AdminSasana relation profile
                AdminSasana.objects.create(
                    account=admin_account,
                    sasana=sasana
                )

                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        sasana = self.get_object()
        if not sasana.admin_sasana:
            return Response({"error": "Sasana ini tidak memiliki Admin."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            account = sasana.admin_sasana
            account.set_password('sasana123')
            account.force_password_change = True
            account.save()
            return Response({"message": "Password admin sasana berhasil direset ke sasana123"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def nearest(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        if not lat or not lng:
            return Response({"error": "Latitude and Longitude are required."}, status=400)
            
        try:
            user_lat = float(lat)
            user_lng = float(lng)
        except ValueError:
            return Response({"error": "Invalid coordinates format."}, status=400)

        sasanas = Sasana.objects.exclude(map__isnull=True).exclude(map='')
        sasana_list = []

        for sasana in sasanas:
            try:
                # Format asumsi map: "-6.6000, 106.8000"
                s_lat_str, s_lng_str = sasana.map.split(',')
                s_lat = float(s_lat_str.strip())
                s_lng = float(s_lng_str.strip())

                # Rumus Haversine sederhana
                R = 6371.0 # Radius bumi dalam km
                dlat = math.radians(s_lat - user_lat)
                dlng = math.radians(s_lng - user_lng)
                a = math.sin(dlat / 2)**2 + math.cos(math.radians(user_lat)) * math.cos(math.radians(s_lat)) * math.sin(dlng / 2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c

                sasana_list.append({
                    'sasana': SasanaSerializer(sasana).data,
                    'distance': distance
                })
            except Exception:
                continue # Abaikan jika format map salah

        # Urutkan berdasarkan jarak dan ambil 10 terdekat
        sasana_list.sort(key=lambda x: x['distance'])
        nearest_sasanas = [item['sasana'] for item in sasana_list[:10]]
        
        return Response(nearest_sasanas)

class PesertaViewSet(viewsets.ModelViewSet):
    queryset = Peserta.objects.all()
    serializer_class = PesertaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nik', 'account__nama']

    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        if hasattr(self.request.user, 'adminsasana'):
            serializer.save(sasana=self.request.user.adminsasana.sasana)
        else:
            if not serializer.validated_data.get('sasana'):
                raise ValidationError({"sasana": ["Sasana ID wajib diisi jika Anda bukan Admin Sasana, atau profil Anda belum terhubung dengan Sasana."]})
            serializer.save()

    def perform_update(self, serializer):
        from rest_framework.exceptions import ValidationError
        if hasattr(self.request.user, 'adminsasana'):
            serializer.save(sasana=self.request.user.adminsasana.sasana)
        else:
            if not serializer.validated_data.get('sasana') and not serializer.instance.sasana:
                raise ValidationError({"sasana": ["Sasana ID tidak boleh kosong."]})
            serializer.save()

class InstrukturViewSet(viewsets.ModelViewSet):
    queryset = Instruktur.objects.all()
    serializer_class = InstrukturSerializer

    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        if hasattr(self.request.user, 'adminsasana'):
            serializer.save(sasana=self.request.user.adminsasana.sasana)
        else:
            if not serializer.validated_data.get('sasana'):
                raise ValidationError({"sasana": ["Sasana ID wajib diisi jika Anda bukan Admin Sasana, atau profil Anda belum terhubung dengan Sasana."]})
            serializer.save()

    def perform_update(self, serializer):
        from rest_framework.exceptions import ValidationError
        if hasattr(self.request.user, 'adminsasana'):
            serializer.save(sasana=self.request.user.adminsasana.sasana)
        else:
            if not serializer.validated_data.get('sasana') and not serializer.instance.sasana:
                raise ValidationError({"sasana": ["Sasana ID tidak boleh kosong."]})
            serializer.save()

class PengurusSasanaViewSet(viewsets.ModelViewSet):
    queryset = PengurusSasana.objects.all()
    serializer_class = PengurusSasanaSerializer

    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        if hasattr(self.request.user, 'adminsasana'):
            serializer.save(sasana=self.request.user.adminsasana.sasana)
        else:
            if not serializer.validated_data.get('sasana'):
                raise ValidationError({"sasana": ["Sasana ID wajib diisi jika Anda bukan Admin Sasana, atau profil Anda belum terhubung dengan Sasana."]})
            serializer.save()

    def perform_update(self, serializer):
        from rest_framework.exceptions import ValidationError
        if hasattr(self.request.user, 'adminsasana'):
            serializer.save(sasana=self.request.user.adminsasana.sasana)
        else:
            if not serializer.validated_data.get('sasana') and not serializer.instance.sasana:
                raise ValidationError({"sasana": ["Sasana ID tidak boleh kosong."]})
            serializer.save()

class KeterbatasanFisikViewSet(viewsets.ModelViewSet):
    queryset = KeterbatasanFisik.objects.all()
    serializer_class = KeterbatasanFisikSerializer

class KendalaKesehatanViewSet(viewsets.ModelViewSet):
    queryset = KendalaKesehatan.objects.all()
    serializer_class = KendalaKesehatanSerializer

class CarouselImageViewSet(viewsets.ModelViewSet):
    queryset = CarouselImage.objects.all()
    serializer_class = CarouselImageSerializer

import urllib.request
import json
from django.http import JsonResponse

import requests
from django.http import JsonResponse

def proxy_wilayah(request, endpoint):
    # Coba sumber utama (emsifa) jika memungkinkan, atau tetap gunakan wilayah.id
    # Kita akan mencoba memetakan endpoint wilayah.id ke emsifa
    # wilayah.id: provinces.json, regencies/{id}.json, districts/{id}.json, villages/{id}.json
    # emsifa: provinces.json, regencies/{id}.json, districts/{id}.json, villages/{id}.json (sama)
    
    primary_url = f"https://www.emsifa.com/api-wilayah-indonesia/api/{endpoint}"
    fallback_url = f"https://wilayah.id/api/{endpoint}"
    
    try:
        # Mencoba primary source
        try:
            response = requests.get(primary_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            response.raise_for_status()
            data = response.json()
        except Exception:
            # Jika primary gagal, coba fallback
            response = requests.get(fallback_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            response.raise_for_status()
            data = response.json()

        # Normalisasi struktur respons
        # 1. Pastikan dalam bentuk {"data": [...]}
        if isinstance(data, list):
            raw_list = data
        elif isinstance(data, dict) and "data" in data:
            raw_list = data["data"]
        else:
            raw_list = [data] if data else []

        # 2. Pastikan setiap item punya 'code' dan 'name'
        # emsifa sering pakai 'id', wilayah.id pakai 'code'
        normalized_data = []
        for item in raw_list:
            if not isinstance(item, dict): continue
            code = str(item.get('code') or item.get('id') or '')
            name = str(item.get('name') or '')
            if code and name:
                normalized_data.append({'code': code, 'name': name})
        
        return JsonResponse({'data': normalized_data}, safe=False)
        
    except Exception as e:
        print(f"Proxy Final Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
