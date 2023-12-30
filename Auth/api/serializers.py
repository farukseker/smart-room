from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Auth.models import OTPDevice


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        # has_otp = OTPDevice.user_has_otp_device(self.user)
        return {
            "username": self.user.username,
            "email": self.user.email,
            "has_otp": False,
            # "otp_verify":
            # "permissions": self.user.user_permissions.values_list("codename", flat=True),
            # "groups": self.user.groups.values_list("name", flat=True),
            **attrs,
        }

