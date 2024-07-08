from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        # Пропускаем анонимных пользователей
        if not request.user.is_authenticated:
            return False

        # Проверяем, является ли пользователь администратором
        return request.user.role == 'admin' or request.user.is_superuser
