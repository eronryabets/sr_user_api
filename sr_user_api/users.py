
class SimpleUser:
    """
    Упрощённое представление аутентифицированного пользователя.

    Атрибуты:
        - `id` (str): Идентификатор пользователя, полученный из JWT-пayload.
        - `username` (str): Имя пользователя, полученное из JWT-пayload.
        - `is_authenticated` (bool): Флаг, указывающий, что пользователь аутентифицирован. Всегда `True`.
    """
    def __init__(self, payload):
        self.id = payload.get('user_id')
        self.username = payload.get('username')
        self.is_authenticated = True


class AnonymousUser:
    """
    Представление неаутентифицированного (анонимного) пользователя.

    Атрибуты:
        - `is_authenticated` (bool): Флаг, указывающий, что пользователь не аутентифицирован. Всегда `False`.
    """
    def __init__(self):
        self.is_authenticated = False
