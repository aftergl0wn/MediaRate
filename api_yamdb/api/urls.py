from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TitelsViewSet, GenresViewSet, CategoriesViewSet

router = DefaultRouter()

router.register('titles', TitelsViewSet)
router.register('genres', GenresViewSet)
router.register('categories', CategoriesViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')), 
    path('v1/', include('djoser.urls.jwt')),
]
