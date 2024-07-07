from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from users.utils import get_confirmation_code
from .serializers import CustomUserSerializer

User = get_user_model()


class CustomTokenObtainPairView(APIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():  # Сначала проверка is_valid
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'Неверное имя пользователя'}, status=status.HTTP_404_NOT_FOUND)

            if (not user.confirmation_code
                    or user.confirmation_code != confirmation_code):
                return Response({'error': 'Неверный код подтверждения'},
                                status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)

            return Response({'access': str(refresh.access_token)})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')

        try:
            # Если пользователь сущетсвует, то проверяем почту,
            # затем обновляем код подтверждения
            user = User.objects.get(username=username)
            if user.email != email:
                return Response({'error': 'Неверный email.'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.confirmation_code = get_confirmation_code()
            user.save()
            serializer = self.serializer_class(user)
        except User.DoesNotExist:
            # Если пользователя не существует, создаем нового
            if serializer.is_valid():
                user = serializer.save()
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        # Отправка email с кодом подтверждения
        subject = 'YaMDB: Подтверждение адреса электронной почты'
        message = (f'''Ваш код подтверждения: {user.confirmation_code}.'
                Используйте этот код для активации вашего аккаунта.''')
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, (email,))

        return Response({'username': serializer.data['username'],
                         'email': serializer.data['email']})
