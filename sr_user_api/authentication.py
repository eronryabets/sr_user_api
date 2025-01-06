import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from sr_user_api.users import SimpleUser
import logging

logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    """
    Класс для аутентификации пользователей с использованием JWT (JSON Web Tokens).

    Этот класс проверяет наличие JWT-токена в cookies (`access_token`) или в заголовке
    `Authorization` запроса. Если токен валиден и не истёк, создаётся объект `SimpleUser`
    с данными пользователя из токена.
    """
    def authenticate(self, request):
        """
        Аутентифицирует пользователя на основе JWT-токена.

        Процесс аутентификации:
            1. Проверяет наличие токена в cookies под ключом `access_token`.
            2. Если токен не найден в cookies, ищет его в заголовке `Authorization`
               в формате `Bearer <token>`.
            3. Если токен найден, декодирует его с использованием секретного ключа
               `JWT_SECRET_KEY` и алгоритма `HS256`.
            4. Если токен действителен, создаёт объект `SimpleUser` с данными пользователя.
            5. Если токен просрочен или неверен, выбрасывает исключение `AuthenticationFailed`.

        :param request: HTTP-запрос, содержащий данные для аутентификации.
        :type request: rest_framework.request.Request
        :return: Кортеж с объектом пользователя и `None`, если аутентификация успешна.
                 Возвращает `None`, если аутентификация не выполнена.
        :rtype: tuple or None

        :raises AuthenticationFailed: Если токен истёк или неверен.
        """
        logger.info("Начало аутентификации в JWTAuthentication")
        token = request.COOKIES.get('access_token')

        if not token:
            logger.info("Токен не найден в cookies, проверяем заголовок Authorization")
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header[7:]
                logger.info("Токен получен из заголовка Authorization")

        if not token:
            logger.warning("Токен не найден ни в cookies, ни в заголовке Authorization")
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            logger.info(f"Токен успешно декодирован: {payload}")
        except jwt.ExpiredSignatureError:
            logger.error("Ошибка аутентификации: срок действия токена истёк")
            raise AuthenticationFailed('Токен истёк')
        except jwt.InvalidTokenError:
            logger.error("Ошибка аутентификации: неверный токен")
            raise AuthenticationFailed('Неверный токен')

        user = SimpleUser(payload)
        logger.info(f"Пользователь успешно аутентифицирован: {user.id}")
        return (user, None)
