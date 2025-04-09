from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from .filters import TitlesFilters
from .mixins import (
    CategoryGenreMixin,
    CreateListDestroyMixin,
    CustomUpdateMixin,
    RetrieveMixin
)
from .permissions import (
    IsAdminOrSuperuser,
    IsAdminOrReadOnlyPermission,
    IsOwnerOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CustomUserSerializer,
    GenereSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleGetSerializer,
    TokenUserSerializer,
    SignUpUserSerializer,
)
from .utils import get_confirmation_code

User = get_user_model()


class ReviewViewSet(CustomUpdateMixin,
                    CreateListDestroyMixin,
                    RetrieveMixin):
    """Создание, изменение и удаление отзывов"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('text', 'author', 'score')
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews_title.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(CustomUpdateMixin,
                     CreateListDestroyMixin,
                     RetrieveMixin):
    """Создание, изменение и удаление комментариев"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('text', 'author',)
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class CustomTokenView(APIView):
    serializer_class = TokenUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        confirmation_code = serializer.validated_data['confirmation_code']
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
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        user.confirmation_code = get_confirmation_code()
        user.save()

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
    def get_me_endpoint(self, request):
        serializer = CustomUserSerializer(
            request.user,
            partial=True,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)


class TitelsViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews_title__score')
                                      ).all().order_by('id')
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilters
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializer
    http_method_names = ['get', 'delete', 'patch', 'post']

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleGetSerializer
        return TitleSerializer


class GenreViewSet(CategoryGenreMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenereSerializer


class CategoryViewSet(CategoryGenreMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', )
