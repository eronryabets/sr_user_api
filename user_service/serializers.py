from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'avatar', 'settings', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'required': True, 'read_only': False},  # Указываем, что поле id обязательно и не read-only
        }

    def create(self, validated_data):
        # Проверяем, что id присутствует и использован для создания
        if 'id' not in validated_data:
            raise serializers.ValidationError({"error": "User ID is required."})

        return super().create(validated_data)