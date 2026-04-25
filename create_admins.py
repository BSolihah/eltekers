import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eltekers.settings')
django.setup()

from sasana.models import Account, AdminDaerah, AdminSasana, Sasana

def create_accounts():
    # Admin Daerah
    u1, created = Account.objects.get_or_create(
        username='admin_daerah', 
        defaults={'nama': 'Admin Daerah', 'role': 'ADMIN_DAERAH'}
    )
    if created:
        u1.set_password('password123')
        u1.save()
        print("Created Admin Daerah: admin_daerah / password123")
    else:
        print("Admin Daerah already exists")
    
    AdminDaerah.objects.get_or_create(account=u1, defaults={'daerah': 'Jawa Barat'})

    # Sasana for Admin Sasana
    s, created = Sasana.objects.get_or_create(
        nama='Sasana Pusat', 
        defaults={
            'propinsi': 'Jawa Barat', 
            'kabupaten': 'Bogor', 
            'kecamatan': 'Bogor Tengah', 
            'kelurahan_desa': 'Pabaton', 
            'map': '0,0'
        }
    )
    if created:
        print("Created Sasana Pusat")

    # Admin Sasana
    u2, created = Account.objects.get_or_create(
        username='admin_sasana', 
        defaults={'nama': 'Admin Sasana', 'role': 'ADMIN_SASANA'}
    )
    if created:
        u2.set_password('password123')
        u2.save()
        print("Created Admin Sasana: admin_sasana / password123")
    else:
        print("Admin Sasana already exists")
    
    AdminSasana.objects.get_or_create(account=u2, sasana=s)

if __name__ == '__main__':
    create_accounts()
