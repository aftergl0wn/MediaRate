from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitelsViewSet,
                    UserViewSet, CommentViewSet, ReviewViewSet,
                    CustomTokenView, SignUpView)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitelsViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/',
         CustomTokenView.as_view(),
         name='token'
         ),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup')
]
