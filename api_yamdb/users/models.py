from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError('Задайте имя пользователя.')
        if not email:
            raise ValueError('Задайте email.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)


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
        ],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.'
        }
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует.'
        },
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField('Биография', blank=True)
    is_staff = models.BooleanField('Суперпользователь', default=False)
    is_active = models.BooleanField('Активен')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        if self.username == 'me':
            raise ValidationError('Использовать имя "me" запрещено.')
        if self.role not in ROLE_CHOICES:
            raise ValidationError('Неверная роль. Допустимые значения:'
                                  'user, moderator, admin.')

    def __str__(self):
        return self.username
