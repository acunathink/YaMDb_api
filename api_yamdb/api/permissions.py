from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Доступ к эндпоинту api/v1/users/ разрешен только для администраторов."""
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.user.is_authenticated
                and request.user.role == 'admin')


class AuthorOrModerPermission(permissions.BasePermission):
    """Изменение объектов доступно только для Автора."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role in ['moderator', 'admin'])


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """POST/DELETE - только для Администраторов, остальные - только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_authenticated
                and request.user.role == 'admin')
