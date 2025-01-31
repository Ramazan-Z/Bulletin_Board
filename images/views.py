from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from images import models, serializers


@extend_schema_view(
    list=extend_schema(
        operation_id="List images",
        description="Просмотр списка изображений. Доступно только авторизованным пользователям.",
    ),
    create=extend_schema(
        operation_id="Add image",
        description="Добавление изображения к объявлению. Возможно добавить только к своим объявлениям.",
    ),
    retrieve=extend_schema(
        operation_id="Get image", description="Просмотр изображения. Доступно только авторизованным пользователям."
    ),
    update=extend_schema(
        operation_id="Update image",
        description="Обновить изображение. Возможно только со своими изображениями.",
    ),
    partial_update=extend_schema(
        operation_id="Edit image",
        description="Редактировать изображение. Возможно только со своими изображениями.",
    ),
    destroy=extend_schema(
        operation_id="Delete image",
        description="Удалить изображение. Возможно только со своими изображениями. Также доступно администратору.",
    ),
)
class ImagesViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с изображениями товаров"""

    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("ad",)
