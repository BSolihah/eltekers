from rest_framework import viewsets, filters
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

class InstrukturViewSet(viewsets.ModelViewSet):
    queryset = Instruktur.objects.all()
    serializer_class = InstrukturSerializer

class PengurusSasanaViewSet(viewsets.ModelViewSet):
    queryset = PengurusSasana.objects.all()
    serializer_class = PengurusSasanaSerializer

class KeterbatasanFisikViewSet(viewsets.ModelViewSet):
    queryset = KeterbatasanFisik.objects.all()
    serializer_class = KeterbatasanFisikSerializer

class KendalaKesehatanViewSet(viewsets.ModelViewSet):
    queryset = KendalaKesehatan.objects.all()
    serializer_class = KendalaKesehatanSerializer

class CarouselImageViewSet(viewsets.ModelViewSet):
    queryset = CarouselImage.objects.all()
    serializer_class = CarouselImageSerializer
