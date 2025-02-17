from rest_framework.permissions import BasePermission


class IsOwnerImage(BasePermission):
    """Определение прав владельца изображения"""

    def has_object_permission(self, request, view, image):
        return image.ad.author == request.user
