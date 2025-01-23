from rest_framework import serializers

from board import models


class AdsListSerializer(serializers.ModelSerializer):
    """Сериализатор списка объявлений."""

    comments_count = serializers.SerializerMethodField()

    @staticmethod
    def get_comments_count(advertisement) -> int:
        return int(advertisement.ad_comments.count())

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

    class Meta:
        model = models.Advertisement
        fields = "__all__"
