from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

# router = SimpleRouter()
# router.register('auth/token', CustomTokenObtainPairViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/',
         views.CustomTokenObtainPairView.as_view(),
         name='token'
         ),
    path('v1/auth/signup/', views.SignUpView.as_view(), name='signup')
]
