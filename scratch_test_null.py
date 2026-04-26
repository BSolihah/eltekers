import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eltekers.settings')
django.setup()

from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from sasana.models import *
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

sasana = Sasana.objects.first()
admin_user = User.objects.filter(role='ADMIN_SASANA').first()

client = APIClient()
client.force_authenticate(user=admin_user)

payload = {
    "account": {"username": "peserta4", "nama": "Peserta 4", "password": "password", "role": "PESERTA"},
    "nik": "1234567890123459",
    "no_hp": "08123456789",
    "tanggal_lahir": "2000-01-01",
    "berat_badan": "60",
    "tinggi_badan": "165",
    "sasana": None  # Simulate null from frontend
}

try:
    response = client.post('/api/peserta/', payload, format='json')
    print("Status:", response.status_code)
    print("Response:", response.data)
except Exception as e:
    print("EXCEPTION CAUGHT IN TEST:", e)
