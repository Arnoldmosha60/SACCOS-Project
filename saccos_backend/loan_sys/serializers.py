from rest_framework import serializers
from user_management.models import User
from .models import Loan, LoanVerification

class LoanSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Loan
        fields = '__all__'

