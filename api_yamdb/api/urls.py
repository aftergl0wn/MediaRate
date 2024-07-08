from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views
from .views import UserViewSet

app_name = 'api'

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/',
         views.CustomTokenView.as_view(),
         name='token'
         ),
    path('v1/auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('v1/', include(router.urls))
]
