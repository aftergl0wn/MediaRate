from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .managers import CustomUserManager

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.MAX_USER_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=('Имя пользователя может содержать только буквы,'
                         'цифры и символы @/./+/-/_.')
            )
        ]
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_USER_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_USER_LENGTH,
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField('Биография', blank=True)
    is_staff = models.BooleanField('Суперпользователь', default=False)
    is_active = models.BooleanField('Активен', default=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.MAX_USER_LENGTH,
        blank=True,
        null=True,
        default=None
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        if self.username.lower() == 'me':
            raise ValidationError('Использовать имя "me" запрещено.')

    def __str__(self):
        return self.username
