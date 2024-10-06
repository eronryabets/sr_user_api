import uuid
from django.db import models


class CustomUser(models.Model):
    # ID, который будет приходить из сервиса авторизации (обязательно должен быть передан)
    id = models.UUIDField(primary_key=True, editable=False)

    # Имя и фамилия пользователя
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    # Аватарка пользователя (загрузка изображений в папку avatars/)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Настройки пользователя в формате JSON
    settings = models.JSONField(default=dict, blank=True)

    # Дата создания пользователя
    created_at = models.DateTimeField(auto_now_add=True)

    # Дата последнего обновления записи пользователя
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    # Вся авторизация через AUTH сервис идет.

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True
