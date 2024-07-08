from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/',
         views.CustomTokenView.as_view(),
         name='token'
         ),
    path('v1/auth/signup/', views.SignUpView.as_view(), name='signup')
]
