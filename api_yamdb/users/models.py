from django.db import models
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
        max_length=150,
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
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
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
    confirmation_code = models.IntegerField(
        'Код подтверждения',
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
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['username', 'email'],
        #         name='unique_user_email'
        #     )
        # ]

    def clean(self):
        if self.username.lower() == 'me':
            raise ValidationError('Использовать имя "me" запрещено.')
        # if self.role not in ROLE_CHOICES:
        #     raise ValidationError('Неверная роль. Допустимые значения:'
        #                           'user, moderator, admin.')

    def __str__(self):
        return self.username
