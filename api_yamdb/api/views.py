from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from users.utils import get_confirmation_code
from .serializers import CustomUserSerializer

User = get_user_model()

