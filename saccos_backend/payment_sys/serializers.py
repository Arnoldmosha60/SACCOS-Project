from rest_framework import serializers
from .models import *

class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = '__all__'

class SaccosWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaccosWallet
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = '__all__'
    