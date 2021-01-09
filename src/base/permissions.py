from rest_framework.permissions import BasePermission


class IsAuthenticatedAndOwner(BasePermission):
    """
    Разрешает доступ только аутентифицированным пользователям и владельцам.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated
                    and (obj.user == request.user))


class IsAdminUser(BasePermission):
    """
    Разрешает доступ администратору
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsStuffUser(BasePermission):
    """
    Разрешает доступ модератору
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_stuff)
