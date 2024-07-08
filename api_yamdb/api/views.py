from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from users.utils import get_confirmation_code
from .serializers import CustomUserSerializer

User = get_user_model()


class CustomTokenObtainPairView(APIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        username = request.data.get('username')
        if not username:
            return JsonResponse({'username': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = request.data.get('confirmation_code')
        if not confirmation_code:
            return JsonResponse({'confirmation_code': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Используем get_object_or_404 для поиска пользователя
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем код подтверждения 
        if not user.confirmation_code or user.confirmation_code != confirmation_code:
            return JsonResponse({'error': 'Invalid confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)

        # Код подтверждения верный
        refresh = RefreshToken.for_user(user)

        # Сбрасываем код подтверждения после использования
        user.confirmation_code = None 
        user.save(update_fields=['confirmation_code'])

        return JsonResponse({
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class SignUpView(APIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')

        try:
            # Если пользователь существует, то проверяем почту,
            # затем обновляем код подтверждения
            user = User.objects.get(username=username)
            if user.email != email:
                return JsonResponse({'error': 'Неверный email.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(user)
        except User.DoesNotExist:
            # Если пользователя не существует, создаем нового
            if serializer.is_valid():
                user = serializer.save()
            else:
                return JsonResponse(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)

        user.confirmation_code = get_confirmation_code()
        user.save()

        # Отправка email с кодом подтверждения
        message = (f'Ваш код подтверждения: {user.confirmation_code}. '
                   'Используйте этот код для активации вашего аккаунта.')
        send_mail(subject='YaMDB: Код подтверждения.',
                  message=message,
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  fail_silently=True
                  )

        return JsonResponse({'username': serializer.data['username'],
                             'email': serializer.data['email']})
