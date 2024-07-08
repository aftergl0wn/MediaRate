from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import ROLE_CHOICES

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role', 'bio', 'confirmation_code')
        validators = []

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено.')
        return value
