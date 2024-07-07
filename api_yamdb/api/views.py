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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')

            user, created = User.objects.get_or_create(username=username)
            confirmation_code = get_confirmation_code()

            user.confirmation_code = confirmation_code
            if created:
                user.email = email
                user.is_active = False
            user.save()

        # Отправка email с кодом подтверждения
            subject = 'YaMDB: Подтверждение адреса электронной почты'
            message = (f'''Ваш код подтверждения: {confirmation_code}.'
                   Используйте этот код для активации вашего аккаунта.''')
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list,
                      fail_silently=False)

            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
