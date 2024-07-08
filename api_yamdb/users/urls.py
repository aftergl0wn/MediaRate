from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('token/',
         views.CustomTokenObtainPairView.as_view(),
         name='token'
         ),
    path('signup/', views.SignUpView.as_view(), name='signup')
]
