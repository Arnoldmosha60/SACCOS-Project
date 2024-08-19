from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            "password": {"write_only": True, "required": False},  # password is not required at creation
            "membership_number": {"required": False},
            "is_active": {"read_only": True},
            "status": {"read_only": True},
            "username": {"required": False}, 
        }

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User(**validated_data)
        user.set_unusable_password()  # set an unusable password initially
        user.save()
        return user

    def get_profile(self, obj):
        request = self.context.get('request')
        # Ensure obj has the attribute 'profile' and it is not None
        if request and hasattr(obj, 'profile') and obj.profile:
            return request.build_absolute_uri(obj.profile.url)
        return None

    def get_contact(self, obj):
        if not isinstance(obj, User):
            print(f"Expected a User instance, but got {type(obj)} instead.")
            return None
        phone_number = getattr(obj, 'phone_number', None)
        if phone_number and phone_number.startswith("255"):
            phone_number = "0" + phone_number[3:]
        return phone_number


class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)
    confirmNewPassword = serializers.CharField(required=True)

    def validate(self, data):
        if data['newPassword'] != data['confirmNewPassword']:
            raise serializers.ValidationError("New password and confirm password do not match")
        return data
        

class UserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'profile']