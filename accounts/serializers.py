from rest_framework import serializers
from rest_framework.permissions import AllowAny
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]
    password = serializers.CharField(max_length=30,
                                     min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'date_joined',
                  'first_name', 'last_name']


class CustomUserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']
