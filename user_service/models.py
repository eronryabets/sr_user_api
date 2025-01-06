import uuid
from django.db import models


class User(models.Model):
    """
    Модель пользователя.

    Поля:
        - `id` (UUIDField): Уникальный идентификатор пользователя, полученный из сервиса авторизации. Обязательное поле.
        - `first_name` (CharField): Имя пользователя. Необязательное поле, максимальная длина 50 символов.
        - `last_name` (CharField): Фамилия пользователя. Необязательное поле, максимальная длина 50 символов.
        - `native_language` (CharField): Родной язык пользователя, на который будут выполняться переводы текста.
         Необязательное поле, максимальная длина 50 символов.
        - `avatar` (ImageField): Аватар пользователя. Загружается в папку `avatars/`. Необязательное поле.
        - `settings` (JSONField): Настройки пользователя в формате JSON. По умолчанию пустой словарь.
        - `created_at` (DateTimeField): Дата и время создания записи пользователя. Автоматически устанавливается при создании.
        - `updated_at` (DateTimeField): Дата и время последнего обновления записи пользователя. Автоматически обновляется при сохранении.
    """

    id = models.UUIDField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    native_language = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

