from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from .utils import get_confirmation_code
from .serializers import (
    CustomUserSerializer,
    TokenUserSerializer,
    SignUpUserSerializer,
)

User = get_user_model()


class CustomTokenObtainPairView(APIView):
    serializer_class = TokenUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=request.data.get('username')
        )
        confirmation_code = request.data.get('confirmation_code')
        if not default_token_generator.check_token(user, confirmation_code):
            return JsonResponse({'confirmation_code': ('Неверный код'
                                                       'подтверждения')},
                                status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({'access': str(refresh.access_token)})


class SignUpView(APIView):
    serializer_class = SignUpUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')

        try:
            # Если пользователь существует, то проверяем почту
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
        confirmation_code = get_confirmation_code(user)

        send_mail(subject='YaMDB: Код подтверждения.',
                  message=f'Ваш код подтверждения: {confirmation_code}.',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  fail_silently=True
                  )

        return JsonResponse({'username': serializer.data['username'],
                             'email': serializer.data['email']})
