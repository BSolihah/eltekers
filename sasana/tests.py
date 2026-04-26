from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Account, Sasana, Peserta
from django.db.utils import IntegrityError
import datetime

class SasanaModelTest(TestCase):
    def setUp(self):
        self.admin_user = Account.objects.create_user(
            username='adminsasana',
            password='password123',
            nama='Admin Sasana 1',
            role='ADMIN_SASANA'
        )
        self.sasana = Sasana.objects.create(
            nama='Sasana Sehat',
            admin_sasana=self.admin_user,
            propinsi='Jawa Barat',
            kabupaten='Bogor',
            kecamatan='Bogor Tengah',
            kelurahan_desa='Paledang',
            map='-6.6000, 106.8000'
        )

    def test_sasana_creation(self):
        """Test if Sasana is created correctly"""
        self.assertEqual(self.sasana.nama, 'Sasana Sehat')
        self.assertEqual(self.sasana.admin_sasana.username, 'adminsasana')

    def test_account_role(self):
        """Test if Account role is assigned correctly"""
        self.assertEqual(self.admin_user.role, 'ADMIN_SASANA')

    def test_cascade_delete_sasana(self):
        """Test if deleting a Sasana handles related Peserta (cascade check)"""
        peserta_user = Account.objects.create_user(username='p1', role='PESERTA')
        Peserta.objects.create(
            account=peserta_user,
            sasana=self.sasana,
            no_hp='081',
            tanggal_lahir=datetime.date(2000, 1, 1),
            nik='1234567890123450',
            berat_badan=60,
            tinggi_badan=160
        )
        self.assertEqual(Peserta.objects.count(), 1)
        self.sasana.delete()
        # Peserta should be deleted due to CASCADE on ForeignKey(Sasana)
        self.assertEqual(Peserta.objects.count(), 0)

class PesertaModelTest(TestCase):
    def setUp(self):
        self.admin_user = Account.objects.create_user(username='admin', role='ADMIN_SASANA')
        self.sasana = Sasana.objects.create(nama='S1', admin_sasana=self.admin_user)
        self.p_user = Account.objects.create_user(username='p1', role='PESERTA')

    def test_peserta_unique_nik(self):
        """Test that duplicate NIK raises IntegrityError"""
        Peserta.objects.create(
            account=self.p_user,
            sasana=self.sasana,
            no_hp='081',
            tanggal_lahir=datetime.date(1990, 1, 1),
            nik='1111222233334444',
            berat_badan=70,
            tinggi_badan=170
        )
        p2_user = Account.objects.create_user(username='p2', role='PESERTA')
        with self.assertRaises(IntegrityError):
            Peserta.objects.create(
                account=p2_user,
                sasana=self.sasana,
                no_hp='082',
                tanggal_lahir=datetime.date(1991, 1, 1),
                nik='1111222233334444', # Duplicate
                berat_badan=71,
                tinggi_badan=171
            )

class SasanaAPITest(APITestCase):
    def setUp(self):
        self.admin_user = Account.objects.create_user(
            username='adminsasana',
            password='password123',
            nama='Admin Sasana 1',
            role='ADMIN_SASANA'
        )
        self.sasana = Sasana.objects.create(
            nama='Sasana Sehat',
            admin_sasana=self.admin_user,
            propinsi='Jawa Barat',
            kabupaten='Bogor',
            map='-6.6, 106.8'
        )
        self.url = '/api/sasana/'

    def test_get_sasana_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_sasana_by_name(self):
        """Test search filter for Sasana name"""
        Sasana.objects.create(nama='Sasana Bugar', propinsi='Jakarta')
        response = self.client.get(self.url + '?search=Sehat')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nama'], 'Sasana Sehat')

class PesertaAPITest(APITestCase):
    def setUp(self):
        self.admin_user = Account.objects.create_user(username='admin', role='ADMIN_SASANA')
        self.sasana = Sasana.objects.create(nama='S1', admin_sasana=self.admin_user)
        self.p_user = Account.objects.create_user(username='p1', nama='Budi', role='PESERTA')
        Peserta.objects.create(
            account=self.p_user,
            sasana=self.sasana,
            no_hp='081',
            tanggal_lahir=datetime.date(1990, 1, 1),
            nik='1234567890123456',
            berat_badan=70,
            tinggi_badan=170
        )
        self.url = '/api/peserta/'

    def test_search_peserta_by_nik(self):
        """Test searching peserta by NIK"""
        response = self.client.get(self.url + '?search=1234567890123456')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nik'], '1234567890123456')

    def test_search_peserta_by_name(self):
        """Test searching peserta by name (via account__nama)"""
        response = self.client.get(self.url + '?search=Budi')
        self.assertEqual(len(response.data), 1)
        # Note: Depending on serializer, the structure might vary. 
        # But queryset search should work.
