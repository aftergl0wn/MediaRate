from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import CustomUser, ROLE_CHOICES


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role', 'bio')
        validators = []

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено.')
        return value
