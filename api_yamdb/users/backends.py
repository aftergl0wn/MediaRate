from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model  # Функция для получения кастомной модели


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()  # Получаем кастомную модель пользователя

        if username is not None:
            try:
                user = User.objects.get(username=username)  # Или email, если используете email для входа
            except User.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user (#20760).
                User().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
