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
        extra_kwargs = {
            'username': {'validators': []},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

class SasanaSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin_sasana.username', read_only=True)
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
    sasana = serializers.PrimaryKeyRelatedField(queryset=Sasana.objects.all(), required=False, allow_null=True)
    class Meta:
        model = PengurusSasana
        fields = '__all__'

    def to_internal_value(self, data):
        if 'account' in data and isinstance(data['account'], str):
            import json
            data = data.copy()
            data['account'] = json.loads(data['account'])
        return super().to_internal_value(data)

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        username = account_data.get('username')
        account = Account.objects.filter(username=username).first()
        if not account:
            account = Account.objects.create_user(**account_data)
        pengurus = PengurusSasana.objects.create(account=account, **validated_data)
        return pengurus

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account', None)
        if account_data:
            account = instance.account
            for attr, value in account_data.items():
                if attr == 'password':
                    account.set_password(value)
                else:
                    setattr(account, attr, value)
            account.save()
        return super().update(instance, validated_data)

class InstrukturSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    sasana = serializers.PrimaryKeyRelatedField(queryset=Sasana.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Instruktur
        fields = '__all__'

    def to_internal_value(self, data):
        if 'account' in data and isinstance(data['account'], str):
            import json
            data = data.copy()
            data['account'] = json.loads(data['account'])
        return super().to_internal_value(data)

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        username = account_data.get('username')
        account = Account.objects.filter(username=username).first()
        if not account:
            account = Account.objects.create_user(**account_data)
        instruktur = Instruktur.objects.create(account=account, **validated_data)
        return instruktur

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account', None)
        if account_data:
            account = instance.account
            for attr, value in account_data.items():
                if attr == 'password':
                    account.set_password(value)
                else:
                    setattr(account, attr, value)
            account.save()
        return super().update(instance, validated_data)

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
    sasana = serializers.PrimaryKeyRelatedField(queryset=Sasana.objects.all(), required=False, allow_null=True)
    keterbatasan = KeterbatasanFisikSerializer(many=True, read_only=True)
    kendala = KendalaKesehatanSerializer(many=True, read_only=True)
    
    class Meta:
        model = Peserta
        fields = '__all__'

    def to_internal_value(self, data):
        if 'account' in data and isinstance(data['account'], str):
            import json
            data = data.copy()
            data['account'] = json.loads(data['account'])
        return super().to_internal_value(data)

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        account = Account.objects.create_user(**account_data)
        peserta = Peserta.objects.create(account=account, **validated_data)
        return peserta

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account', None)
        if account_data:
            account = instance.account
            for attr, value in account_data.items():
                if attr == 'password':
                    account.set_password(value)
                else:
                    setattr(account, attr, value)
            account.save()
        return super().update(instance, validated_data)

class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = '__all__'
