from rest_framework import serializers

from images import models, validators


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений товаров."""

    def get_validators(self):
        return [validators.ImageValidator(self.context)]

    class Meta:
        model = models.Image
        fields = "__all__"


class AdImagesSerializer(serializers.ModelSerializer):
    """Сериализатор изображений для вложения в просмотр объявления."""

    class Meta:
        model = models.Image
        fields = ("id", "image")
