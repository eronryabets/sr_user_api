from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели `User`.

    Этот сериализатор отвечает за преобразование данных модели `User` в формат JSON и обратно,
    обеспечивая валидацию входящих данных при создании и обновлении пользователей.

    Поля:
        - `id` (UUIDField): Уникальный идентификатор пользователя. Обязательное поле для создания.
        - `first_name` (CharField): Имя пользователя. Необязательное поле.
        - `last_name` (CharField): Фамилия пользователя. Необязательное поле.
        - `native_language` (CharField): Родной язык пользователя для переводов. Необязательное поле.
        - `avatar` (ImageField): Аватар пользователя. Необязательное поле, загружается в папку `avatars/`.
        - `settings` (JSONField): Настройки пользователя в формате JSON. По умолчанию пустой словарь.
        - `created_at` (DateTimeField): Дата и время создания записи пользователя. Только для чтения.
        - `updated_at` (DateTimeField): Дата и время последнего обновления записи пользователя. Только для чтения.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'native_language', 'avatar', 'settings', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'required': True, 'read_only': False},  # Указываем, что поле id обязательно и не read-only
        }

    def create(self, validated_data):
        """
        Создаёт новый экземпляр модели `User` с предоставленными валидированными данными.

        Переопределяет метод `create` для обеспечения обязательного наличия поля `id`.

        :param validated_data: Валидированные данные для создания пользователя.
        :type validated_data: dict
        :return: Созданный экземпляр пользователя.
        :rtype: User
        :raises serializers.ValidationError: Если поле `id` отсутствует в данных.
        """
        # Проверяем, что id присутствует и использован для создания
        if 'id' not in validated_data:
            raise serializers.ValidationError({"error": "User ID is required."})

        return super().create(validated_data)