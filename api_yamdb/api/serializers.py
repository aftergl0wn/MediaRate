import datetime as dt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField

from reviews.models import Titles, Genres, Categories, Comment, Review
from users.models import ROLE_CHOICES


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        author = self.context.get('request').user
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    f'Вы уже оценили произведение: {title}!')
            return data
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class TokenUserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z'
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpUserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=settings.MAX_USER_LENGTH
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError(
                    {'email': 'Неверный email'},
                    status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(username=username)
            if user.username != username:
                raise serializers.ValidationError(
                    {'username': 'Имя пользователя уже существует'},
                    status.HTTP_400_BAD_REQUEST)
        return data

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено.')
        return value


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role', 'bio')


class GenereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug',)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class TitlesGetSerializer(serializers.ModelSerializer):
    genre = GenereSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genres.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Categories.objects.all())

    class Meta:
        model = Titles
        fields = '__all__'

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год!')
        return value

    def validate_rating(self, value):
        if value == 0:
            return None
        return value
