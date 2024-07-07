from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, **extra_fields):
        if not username:
            raise ValueError('Задайте имя пользователя.')
        if not email:
            raise ValueError('Задайте email.')
        email = self.normalize_email(email)
        # extra_fields.setdefault('is_active', False)
        user = self.model(username=username, email=email, **extra_fields)
        user.save()
        return user

    def create_superuser(self, username, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, **extra_fields)
