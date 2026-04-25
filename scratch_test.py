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

try:
    sasana = Sasana.objects.first()
    if not sasana:
        sasana = Sasana.objects.create(nama="Test Sasana")
    
    admin_user = User.objects.filter(role='ADMIN_SASANA').first()
    if not admin_user:
        admin_user = User.objects.create(username="admin_test", role='ADMIN_SASANA')
        AdminSasana.objects.create(account=admin_user, sasana=sasana)
    
    print("Admin Sasana:", admin_user.username, "Sasana ID:", sasana.id)
    
    client = APIClient()
    client.force_authenticate(user=admin_user)
    
    payload = {
        "account": {"username": "peserta2", "nama": "Peserta 2", "password": "password", "role": "PESERTA"},
        "nik": "1234567890123457",
        "no_hp": "08123456789",
        "tanggal_lahir": "2000-01-01",
        "berat_badan": "60",
        "tinggi_badan": "165",
        "sasana": sasana.id
    }
    
    response = client.post('/api/peserta/', payload, format='json')
    print("Status:", response.status_code)
    try:
        print("Response:", response.data)
    except:
        print("Response:", response.content)

except Exception as e:
    import traceback
    traceback.print_exc()
