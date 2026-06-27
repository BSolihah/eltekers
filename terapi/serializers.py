from rest_framework import serializers
from .models import GerakanAcuan, Testimoni, JadwalTerapiSasana, TerapiPeserta, EvaluasiGerakan

class GerakanAcuanSerializer(serializers.ModelSerializer):
    kategori_display = serializers.CharField(source='get_kategori_display', read_only=True)
    class Meta:
        model = GerakanAcuan
        fields = '__all__'

class TestimoniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimoni
        fields = '__all__'

class JadwalTerapiSasanaSerializer(serializers.ModelSerializer):
    sasana_nama = serializers.CharField(source='sasana.nama', read_only=True)
    instruktur_nama = serializers.CharField(source='instruktur.account.nama', read_only=True)
    class Meta:
        model = JadwalTerapiSasana
        fields = '__all__'

class TerapiPesertaSerializer(serializers.ModelSerializer):
    peserta_nama = serializers.CharField(source='peserta.account.nama', read_only=True)
    jadwal_info = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TerapiPeserta
        fields = '__all__'

    def get_jadwal_info(self, obj):
        return f"{obj.jadwal.sasana.nama} - {obj.jadwal.hari} {obj.jadwal.jam_mulai}"

class EvaluasiGerakanSerializer(serializers.ModelSerializer):
    gerakan_nama = serializers.CharField(source='gerakan_acuan.nama_gerakan', read_only=True)
    peserta_nama = serializers.CharField(source='terapi_peserta.peserta.account.nama', read_only=True)
    instruktur_nama = serializers.CharField(source='instruktur.account.nama', read_only=True)
    kesesuaian_display = serializers.CharField(source='get_kesesuaian_display', read_only=True)
    class Meta:
        model = EvaluasiGerakan
        fields = '__all__'
