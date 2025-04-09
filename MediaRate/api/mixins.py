from rest_framework import filters, mixins, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnlyPermission


class CreateListDestroyMixin(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             GenericViewSet):
    pass


class RetrieveMixin(mixins.RetrieveModelMixin,
                    GenericViewSet):
    pass


class CustomUpdateMixin(mixins.UpdateModelMixin,
                        GenericViewSet):

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return super().update(request, *args, **kwargs)


class CategoryGenreMixin(CreateListDestroyMixin):
    permission_classes = (IsAdminOrReadOnlyPermission, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
