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
router.register(r'carousel', api_views.CarouselImageViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/proxy-wilayah/<path:endpoint>', api_views.proxy_wilayah, name='proxy_wilayah'),
    
    # Template Views
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('register/', views.register_view, name='register'),
    path('dashboard/daerah/', views.dashboard_daerah, name='dashboard_daerah'),
    path('dashboard/sasana/', views.dashboard_sasana, name='dashboard_sasana'),
]
