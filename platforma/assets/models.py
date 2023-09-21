from django.db import models

class SessionProfile(models.Model):
    """
    Модель сессии пользователя.

    Attributes:
        user_id (IntegerField): ID пользователя.
        session_key (CharField): Ключ сессии.
        ip_address (CharField): IP-адрес пользователя.
        last_accessed (DateTimeField): Дата и время последнего доступа.

    Methods:
        __str__(): Возвращает строковое представление объекта профиля сессии.
    """
    user_id = models.IntegerField()
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.CharField(max_length=20)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_key