from rest_framework import viewsets, filters
from .models import (
    Account, Sasana, AdminDaerah, AdminSasana, 
    PengurusSasana, Instruktur, Peserta, 
    KeterbatasanFisik, KendalaKesehatan
)
from .serializers import (
    AccountSerializer, SasanaSerializer, AdminDaerahSerializer, 
    AdminSasanaSerializer, PengurusSasanaSerializer, 
    InstrukturSerializer, PesertaSerializer,
    KeterbatasanFisikSerializer, KendalaKesehatanSerializer
)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class SasanaViewSet(viewsets.ModelViewSet):
    queryset = Sasana.objects.all()
    serializer_class = SasanaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'propinsi', 'kabupaten', 'kecamatan', 'kelurahan_desa', 'map']

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
