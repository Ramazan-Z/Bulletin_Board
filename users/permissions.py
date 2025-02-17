from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Определение прав администратора"""

    def has_permission(self, request, view):
        user = request.user
        return user.role == "admin"


class IsOwnerUser(BasePermission):
    """Определение прав владельца"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj
