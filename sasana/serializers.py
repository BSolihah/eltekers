from rest_framework import serializers
from .models import (
    Account, Sasana, AdminDaerah, AdminSasana, 
    PengurusSasana, Instruktur, Peserta, 
    KeterbatasanFisik, KendalaKesehatan, CarouselImage
)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'nama', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

class SasanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sasana
        fields = '__all__'

class AdminDaerahSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = AdminDaerah
        fields = '__all__'

class AdminSasanaSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = AdminSasana
        fields = '__all__'

class PengurusSasanaSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = PengurusSasana
        fields = '__all__'

class InstrukturSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = Instruktur
        fields = '__all__'

class KeterbatasanFisikSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeterbatasanFisik
        fields = '__all__'

class KendalaKesehatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = KendalaKesehatan
        fields = '__all__'

class PesertaSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    keterbatasan = KeterbatasanFisikSerializer(many=True, read_only=True)
    kendala = KendalaKesehatanSerializer(many=True, read_only=True)
    
    class Meta:
        model = Peserta
        fields = '__all__'

class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = '__all__'
