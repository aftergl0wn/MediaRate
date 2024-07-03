from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        if self.username == 'me':
            raise ValidationError('Использовать имя "me" запрещено.')
