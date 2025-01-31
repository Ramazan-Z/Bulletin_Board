from rest_framework import serializers

from images import models


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений товаров."""

    class Meta:
        model = models.Image
        fields = "__all__"


class AdImagesSerializer(serializers.ModelSerializer):
    """Сериализатор изображений для вложения в просмотр объявления."""

    class Meta:
        model = models.Image
        fields = ("id", "image")
