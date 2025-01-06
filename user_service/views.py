from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


# Создание нового пользователя в "Юзер Сервисе"
class CreateUserView(generics.CreateAPIView):
    """
    Представление для создания нового пользователя в "Юзер Сервисе".

    Позволяет любому пользователю (независимо от аутентификации) создавать новый профиль пользователя
    после успешной авторизации через внешний сервис.

    Атрибуты:
        - `queryset` (QuerySet): Набор всех пользователей.
        - `serializer_class` (UserSerializer): Сериализатор для валидации и сохранения данных пользователя.
        - `permission_classes` (list): Разрешения для доступа к представлению. В данном случае доступ разрешён всем.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Так как создается после авторизации, доступ для всех

    def create(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запросы для создания нового пользователя.

        Процесс:
            1. Валидирует входящие данные с помощью `UserSerializer`.
            2. Если данные валидны, создаёт нового пользователя.
            3. Возвращает данные созданного пользователя с кодом статуса `201 CREATED`.

        :param request: HTTP-запрос, содержащий данные для создания пользователя.
        :type request: rest_framework.request.Request
        :return: Response объект с данными созданного пользователя или ошибками валидации.
        :rtype: rest_framework.response.Response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Просмотр и обновление профиля пользователя
class UserProfileView(APIView):
    """
    Представление для просмотра и обновления профиля аутентифицированного пользователя.

    Позволяет аутентифицированным пользователям получать и обновлять свои личные данные.

    Атрибуты:
        - `permission_classes` (list): Разрешения для доступа к представлению. Только аутентифицированные
         пользователи имеют доступ.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Обрабатывает GET-запросы для получения профиля текущего пользователя.

        Процесс:
            1. Ищет пользователя по `id`, соответствующему текущему аутентифицированному пользователю.
            2. Если пользователь найден, возвращает его данные.
            3. Если пользователь не найден, возвращает ошибку `404 NOT FOUND`.

        :param request: HTTP-запрос.
        :type request: rest_framework.request.Request
        :return: Response объект с данными пользователя или сообщением об ошибке.
        :rtype: rest_framework.response.Response
        """
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

    def patch(self, request):
        """
        Обрабатывает PATCH-запросы для частичного обновления профиля текущего пользователя.

        Процесс:
            1. Ищет пользователя по `id`, соответствующему текущему аутентифицированному пользователю.
            2. Если пользователь найден, валидирует входящие данные с помощью `UserSerializer`.
            3. Если данные валидны, обновляет профиль пользователя.
            4. Возвращает обновлённые данные пользователя.
            5. Если пользователь не найден, возвращает ошибку `404 NOT FOUND`.

        :param request: HTTP-запрос, содержащий данные для обновления пользователя.
        :type request: rest_framework.request.Request
        :return: Response объект с обновлёнными данными пользователя или сообщением об ошибке.
        :rtype: rest_framework.response.Response
        """
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
