from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views, views

router = DefaultRouter()
router.register(r'accounts', api_views.AccountViewSet)
router.register(r'sasana', api_views.SasanaViewSet)
router.register(r'peserta', api_views.PesertaViewSet)
router.register(r'instruktur', api_views.InstrukturViewSet)
router.register(r'pengurus-sasana', api_views.PengurusSasanaViewSet)
router.register(r'keterbatasan-fisik', api_views.KeterbatasanFisikViewSet)
router.register(r'kendala-kesehatan', api_views.KendalaKesehatanViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Template Views
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/daerah/', views.dashboard_daerah, name='dashboard_daerah'),
    path('dashboard/sasana/', views.dashboard_sasana, name='dashboard_sasana'),
]
