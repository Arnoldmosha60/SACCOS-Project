from .models import Share, Saving, Event
from rest_framework import serializers

class SharePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'

class SavingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'