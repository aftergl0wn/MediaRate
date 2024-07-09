from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminOrSuperuser
from .serializers import (
    CustomUserSerializer,
    TokenUserSerializer,
    SignUpUserSerializer,
)
from .utils import get_confirmation_code

User = get_user_model()


class CustomTokenView(APIView):
    serializer_class = TokenUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=request.data.get('username')
        )
        confirmation_code = request.data.get('confirmation_code')
        if user.confirmation_code != confirmation_code:
            return JsonResponse({'confirmation_code': ('Неверный код'
                                                       'подтверждения')},
                                status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({'access': str(refresh.access_token)})


class SignUpView(APIView):
    serializer_class = SignUpUserSerializer
    permission_classes = (AllowAny,)

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
                user.confirmation_code = get_confirmation_code()
                user.save()
            else:
                return JsonResponse(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)

        send_mail(subject='YaMDB: Код подтверждения.',
                  message=f'Ваш код подтверждения: {user.confirmation_code}.',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  fail_silently=True
                  )

        return JsonResponse({'username': serializer.data['username'],
                             'email': serializer.data['email']})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperuser,)
    http_method_names = ['get', 'delete', 'patch', 'post']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username', 'email')
    search_fields = ('username', 'email')

    @action(
        methods=('get', 'patch',),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_me_enpoint(self, request):
        serializer = CustomUserSerializer(
            request.user,
            partial=True,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        if self.request.method == 'PATCH':
            if 'role' in request.data:
                raise ValidationError({'role': ('У вас нет прав'
                                                'на изменение роли')})
            serializer.save()
        return JsonResponse(serializer.data)
