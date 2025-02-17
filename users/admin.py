from django.contrib import admin

from users.models import User, WaitingConfirmEmail


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Регистрация пользователя в админке."""

    list_display = ("id", "email", "username")
    list_filter = ("role",)


@admin.register(WaitingConfirmEmail)
class WaitingConfirmEmailAdmin(admin.ModelAdmin):
    """Регистрация модели ожидания подтверждений в админке."""

    list_display = ("id", "new_email", "user")
