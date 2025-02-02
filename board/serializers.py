from rest_framework import serializers

from board import models, validators
from images.serializers import AdImagesSerializer


class AdsListSerializer(serializers.ModelSerializer):
    """Сериализатор списка объявлений."""

    comments_count = serializers.SerializerMethodField()
    images_count = serializers.SerializerMethodField()

    @staticmethod
    def get_comments_count(advertisement) -> int:
        return int(advertisement.ad_comments.count())

    @staticmethod
    def get_images_count(advertisement) -> int:
        return int(advertisement.images.count())

    class Meta:
        model = models.Advertisement
        fields = "__all__"


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор создания и редактирования объявлений."""

    class Meta:
        model = models.Advertisement
        fields = "__all__"
        read_only_fields = ("created_at", "author")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов/коментариев."""

    class Meta:
        model = models.Comment
        fields = "__all__"
        read_only_fields = ("created_at", "author")


class AdRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор деталей объявления."""

    comments = CommentSerializer(many=True, read_only=True, source="ad_comments")
    images = AdImagesSerializer(many=True, read_only=True)

    class Meta:
        model = models.Advertisement
        fields = "__all__"


class SendMessageSerializer(serializers.Serializer):
    """Сериализатор отправки сообщений."""

    result = serializers.SerializerMethodField(label="Information about the result of the request.")
    message = serializers.CharField(write_only=True, label="Message for the recipient.")

    @staticmethod
    def get_result(data) -> str:
        return "Your message has been sent."

    def get_validators(self):
        return [validators.OnlySelfAdValidator(self.context)]

    class Meta:
        fields = "__all__"
