from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import models, serializers, tasks
from users.permissions import IsAdminUser, IsOwnerUser


@extend_schema_view(get=extend_schema(operation_id="Users list"))
class UsersList(generics.ListAPIView):
    """
    Постраничный просмотр списка пользователей.
    Принимает параметры пагинации, сортировки, фильтрации и поисковый запрос.
    Доступно только администратору.
    """

    queryset = models.User.objects.filter(is_superuser=False)
    serializer_class = serializers.UserListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    ordering_fields = ("id", "username")
    search_fields = ("username", "city")
    filterset_fields = ("role",)


@extend_schema_view(post=extend_schema(operation_id="User registration"))
class UserRegister(generics.CreateAPIView):
    """
    Принимает набор учетных данных для регистрации пользователя
    и возвращает JSON ответ с данными успешной регистрации.
    Необходима верификация электронной почты.
    """

    queryset = models.User.objects.filter(is_superuser=False)
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Создание пользователя и генерация токена верификации"""
        user = serializer.save(is_active=False)
        token = AccessToken.for_user(user)
        waiting_confirm = models.WaitingConfirmEmail.objects.create(user=user, token=token)
        tasks.send_verify_email(self.request, waiting_confirm)


@extend_schema_view(get=extend_schema(operation_id="User profile"))
class UserProfile(generics.RetrieveAPIView):
    """Просмотр профиля пользователя. Доступно только владельцу и администратору."""

    queryset = models.User.objects.filter(is_superuser=False)
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsOwnerUser]


@extend_schema_view(
    put=extend_schema(operation_id="Update profile"),
    patch=extend_schema(operation_id="Edit profile"),
)
class UserUpdate(generics.UpdateAPIView):
    """
    Принимает набор учетных данных для редактирования профиля и возвращает JSON
    ответ с данными успешного обновления. При смене эл. почты необходима верификация.
    Доступно только владельцу профиля.
    """

    queryset = models.User.objects.filter(is_superuser=False)
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [IsAuthenticated, IsOwnerUser]

    def perform_update(self, serializer):
        """Логика смены email и пароля"""
        password = serializer.validated_data.pop("password", None)
        email = serializer.validated_data.pop("email", None)
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        if email and email != user.email:
            token = AccessToken.for_user(user)
            waiting_confirm = models.WaitingConfirmEmail.objects.create(user=user, token=token, new_email=email)
            tasks.send_verify_email(self.request, waiting_confirm)


@extend_schema_view(delete=extend_schema(operation_id="User delete"))
class UserDestroy(generics.DestroyAPIView):
    """Удаление аккаунта. Доступно только владельцу профиля."""

    queryset = models.User.objects.filter(is_superuser=False)
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [IsAuthenticated, IsOwnerUser]


@extend_schema_view(post=extend_schema(operation_id="User login"))
class UserLogin(TokenObtainPairView):
    pass


@extend_schema_view(post=extend_schema(operation_id="Token refresh"))
class TokenRefresh(TokenRefreshView):
    pass


class VerifyEmail(generics.GenericAPIView):
    """
    Исключает возможность регистрации аккаунта на несуществующий Email,
    или к которому нет доступа.
    """

    queryset = models.WaitingConfirmEmail.objects.all()
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="Verify email (get)",
        parameters=[
            OpenApiParameter(
                name="token",
                location=OpenApiParameter.QUERY,
                description="Secret confirmation code.",
                required=True,
                type=str,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        """Подтветждение электронной почты по прямой ссылке."""
        token = request.GET.get("token")
        return self.email_activate(token)

    @extend_schema(operation_id="Verify email (post)")
    def post(self, request, *args, **kwargs):
        """Подтветждение электронной почты через POST запрос."""
        token = request.data.get("token")
        return self.email_activate(token)

    def email_activate(self, token):
        """Верификация токена и активация подтверждений"""
        waiting_confirm = self.get_object()
        confirm_data = self.get_serializer(waiting_confirm).data
        user = models.User.objects.get(pk=confirm_data.get("user"))
        new_email = waiting_confirm.new_email

        try:
            user_id = AccessToken(token).payload.get("user_id")
            if user.pk != user_id:
                raise TokenError("This is not your token.")
            if new_email:  # Обновление email.
                user.email = new_email
                confirm_data["result"] = "Successful email address change."
            else:  # Активация аккаунта.
                user.is_active = True
                confirm_data["result"] = "Successful account activation."
            user.save()
            waiting_confirm.delete()
            return response.Response(confirm_data)
        except TokenError as e:
            return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(generics.GenericAPIView):
    """Сброс пароля пользователя через Email."""

    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = [AllowAny]

    @extend_schema(operation_id="Reset password")
    def post(self, request, *args, **kwargs):
        """Отправляет на указанный Email ссылку для востановления пароля."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(models.User, email=serializer.validated_data.get("email"))
        token = AccessToken.for_user(user)
        tasks.send_reset_password_link(request, user, token)

        return response.Response({"result": "The link was sent to the specified email."})


class ResetPasswordConfirm(generics.GenericAPIView):
    """Подтветждение сброса пароля через Email."""

    serializer_class = serializers.ResetPasswordConfirmSerializer
    permission_classes = [AllowAny]

    @extend_schema(operation_id="Reset password confirm")
    def post(self, request, *args, **kwargs):
        """
        Принимает идентификатор пользователя, токен подтверждения и новый пароль.
        Возвращает сообщение о результате запроса.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(models.User, pk=serializer.validated_data.get("user_id"))
        token = serializer.validated_data.get("token")
        new_password = serializer.validated_data.get("new_password")

        try:
            user_id = AccessToken(token).payload.get("user_id")
            if user.pk != user_id:
                raise TokenError("This is not your token.")
            user.is_active = True  # Возможность активации через сброс пароля
            user.set_password(new_password)
            user.save()
            return response.Response({"result": "Password changed successfully"})
        except TokenError as e:
            return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    put=extend_schema(operation_id="User Administration (put)"),
    patch=extend_schema(operation_id="User Administration (patch)"),
)
class AdminManagement(generics.UpdateAPIView):
    """
    Управление ролью и активностью пользователя.
    Доступно только администратору.
    """

    queryset = models.User.objects.filter(is_superuser=False)
    serializer_class = serializers.AdminManagementSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
