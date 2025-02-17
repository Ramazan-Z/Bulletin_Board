from rest_framework import serializers

from board.serializers import AdSerializer, CommentSerializer
from users import models, utils


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор списка пользователей."""

    ads_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    @staticmethod
    def get_ads_count(user) -> int:
        return int(user.ads.count())

    @staticmethod
    def get_comments_count(user) -> int:
        return int(user.comments.count())

    class Meta:
        model = models.User
        fields = ("id", "ads_count", "comments_count", "username", "email", "phone", "city", "role")


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации и редактирования пользователя."""

    def create(self, validated_data):
        phone = validated_data.pop("phone", None)
        validated_data["phone"] = utils.normalize_phone(phone)
        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        phone = validated_data.pop("phone", None)
        validated_data["phone"] = utils.normalize_phone(phone)
        return super().update(instance, validated_data)

    class Meta:
        model = models.User
        exclude = ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")
        read_only_fields = ("date_joined", "last_login", "role")
        extra_kwargs = {"password": {"write_only": True}}


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""

    ads = AdSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        exclude = ("is_superuser", "is_staff", "is_active", "groups", "user_permissions", "password")


class VerifyEmailSerializer(serializers.ModelSerializer):
    """Сериализатор верификации электронной почты."""

    result = serializers.CharField(max_length=40, read_only=True, label="Information about the result of the request.")

    class Meta:
        model = models.WaitingConfirmEmail
        fields = ("user", "result", "token")
        read_only_fields = ("user", "result")
        extra_kwargs = {"token": {"write_only": True, "required": True}}


class ResetPasswordSerializer(serializers.Serializer):
    """Сериализатор запроса сброса пароля."""

    result = serializers.CharField(max_length=41, read_only=True, label="Information about the result of the request.")
    email = serializers.EmailField(write_only=True, required=True, label="User's email address")


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """Сериализатор подтверждения сброса пароля."""

    result = serializers.CharField(max_length=41, read_only=True, label="Information about the result of the request.")
    user_id = serializers.IntegerField(write_only=True, required=True, label="User id")
    token = serializers.CharField(max_length=500, write_only=True, required=True, label="Secret confirmation code.")
    new_password = serializers.CharField(max_length=150, write_only=True, required=True, label="New password")


class AdminManagementSerializer(serializers.ModelSerializer):
    """
    Сериализатор редактирования пользователя для администраторов.
    Обеспечивает возможность блокировки пользователей и назначение новых администраторов.
    """

    class Meta:
        model = models.User
        exclude = ("is_superuser", "is_staff", "groups", "user_permissions", "password")
        read_only_fields = (
            "last_login",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "email",
            "phone",
            "city",
            "avatar",
        )
