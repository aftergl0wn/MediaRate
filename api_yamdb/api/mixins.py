from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet


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
