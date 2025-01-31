from django.contrib import admin

from images.models import Image


@admin.register(Image)
class AdvertisementAdmin(admin.ModelAdmin):
    """Регистрация модели изображений в админке."""

    list_display = ("id", "ad")
