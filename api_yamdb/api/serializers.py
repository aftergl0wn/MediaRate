from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Genre, Category, Comment, Review


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
        title = get_object_or_404(Title, pk=title_id)
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
        max_length=settings.MAX_USER_LENGTH,
        validators=[]
    )
    email = serializers.EmailField(
        max_length=settings.MAX_EMAIL_LENGTH,
        validators=[]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user = User.objects.filter(username=username).first()
        if user is not None and user.email != email:
            raise serializers.ValidationError(
                {'error': 'Email пользователя указан неверно.'},
                status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user is not None and user.username != username:
            raise serializers.ValidationError(
                {'error': 'Пользователь с таким email уже существует.'},
                status.HTTP_400_BAD_REQUEST)
        return data

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено.')
        return value


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role', 'bio')

    def validate(self, data):
        if (self.context.get('request').method == 'PATCH'
            and 'role' in data
                and not self.context.get('request').user.is_admin):
            raise serializers.ValidationError(
                {'role': 'У вас нет прав на изменение роли'})
        return data


class GenereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenereSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value < 1900 or value > timezone.now().year:
            raise serializers.ValidationError('Проверьте год!')
        return value
