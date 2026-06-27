from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    GerakanAcuanViewSet, TestimoniViewSet, JadwalTerapiSasanaViewSet,
    TerapiPesertaViewSet, EvaluasiGerakanViewSet
)
from . import views

router = DefaultRouter()
router.register(r'gerakan', GerakanAcuanViewSet, basename='gerakan')
router.register(r'testimoni', TestimoniViewSet, basename='testimoni')
router.register(r'jadwal', JadwalTerapiSasanaViewSet, basename='jadwal')
router.register(r'sesi-peserta', TerapiPesertaViewSet, basename='sesi-peserta')
router.register(r'evaluasi', EvaluasiGerakanViewSet, basename='evaluasi')

urlpatterns = [
    path('api/', include(router.urls)),
    path('gerakan/', views.gerakan_katalog_view, name='terapi_gerakan_katalog'),
    path('testimoni/', views.testimoni_katalog_view, name='terapi_testimoni_katalog'),
    path('manage/gerakan/', views.gerakan_manage_view, name='terapi_gerakan_manage'),
    path('manage/testimoni/', views.testimoni_manage_view, name='terapi_testimoni_manage'),
    path('manage/jadwal/', views.jadwal_manage_view, name='terapi_jadwal_manage'),
    path('evaluasi/', views.evaluasi_peserta_view, name='terapi_evaluasi_peserta'),
]
