from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Categories, Comment, Genres, Review, Title
from .filters import TitlesFilters
from .mixins import CreateListDestroyMixin, CustomUpdateMixin, RetrieveMixin
from .permissions import (
    IsAdminOrSuperuser,
    IsAdminOrReadOnlyPermission,
    IsOwnerOrReadOnly
)
from .serializers import (
    CategoriesSerializer,
    CommentSerializer,
    CustomUserSerializer,
    GenereSerializer,
    ReviewSerializer,
    TitlesSerializer,
    TitlesGetSerializer,
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
    def get_me_endpoint(self, request):
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


class TitelsViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews_title__score')
                                      ).all().order_by('id')
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilters
    pagination_class = PageNumberPagination
    serializer_class = TitlesSerializer
    http_method_names = ['get', 'delete', 'patch', 'post']

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitlesGetSerializer
        return TitlesSerializer


class GenresViewSet(CreateListDestroyMixin):
    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenereSerializer
    permission_classes = (IsAdminOrReadOnlyPermission, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoriesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnlyPermission, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', )
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
