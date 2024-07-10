from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from api.premissions import IsAdminOrReadOnlyPermission
from api.serializers import (TitlesGetSerializer, TitlesSerializer,
                             GenereSerializer, CategoriesSerializer)
from api.filters import TitlesFilters
from reviews.models import Titles, Genres, Categories


class TitelsViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().order_by('id')
    permission_classes = (IsAdminOrReadOnlyPermission, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilters
    pagination_class = PageNumberPagination
    serializer_class = TitlesSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitlesGetSerializer
        return TitlesSerializer


class GenresViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenereSerializer
    permission_classes = (IsAdminOrReadOnlyPermission, )
    pagination_class = PageNumberPagination


class CategoriesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnlyPermission, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', )
    search_fields = ('name',)
