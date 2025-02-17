from django.contrib import admin

from board.models import Advertisement, Comment


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """Регистрация модели объявлений в админке."""

    list_display = ("id", "title", "author")
    search_fields = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Регистрация модели отзывов в админке."""

    list_display = ("id", "text", "author")
    search_fields = ("text",)
