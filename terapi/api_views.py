from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import GerakanAcuan, Testimoni, JadwalTerapiSasana, TerapiPeserta, EvaluasiGerakan
from .serializers import (
    GerakanAcuanSerializer, TestimoniSerializer, JadwalTerapiSasanaSerializer,
    TerapiPesertaSerializer, EvaluasiGerakanSerializer
)

class GerakanAcuanViewSet(viewsets.ModelViewSet):
    queryset = GerakanAcuan.objects.all().order_by('-created_at')
    serializer_class = GerakanAcuanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategori']

class TestimoniViewSet(viewsets.ModelViewSet):
    queryset = Testimoni.objects.all().order_by('-created_at')
    serializer_class = TestimoniSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_published', 'peserta']

class JadwalTerapiSasanaViewSet(viewsets.ModelViewSet):
    queryset = JadwalTerapiSasana.objects.all()
    serializer_class = JadwalTerapiSasanaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sasana', 'instruktur', 'hari']

class TerapiPesertaViewSet(viewsets.ModelViewSet):
    queryset = TerapiPeserta.objects.all()
    serializer_class = TerapiPesertaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['jadwal', 'peserta', 'status_kehadiran']

class EvaluasiGerakanViewSet(viewsets.ModelViewSet):
    queryset = EvaluasiGerakan.objects.all().order_by('-tanggal_evaluasi')
    serializer_class = EvaluasiGerakanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['terapi_peserta', 'gerakan_acuan', 'instruktur', 'kesesuaian']
