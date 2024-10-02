from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'avatar', 'settings', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
