from rest_framework.permissions import BasePermission


class IsAuthorUser(BasePermission):
    """Определение прав автора"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
