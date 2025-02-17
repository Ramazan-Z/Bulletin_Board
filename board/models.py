from django.conf import settings
from django.db import models


class Advertisement(models.Model):
    """Модель сущности объявления"""

    title: models.Field = models.CharField(
        max_length=150,
        verbose_name="Title",
        help_text="Название товара или услуги.",
    )
    description: models.Field = models.TextField(
        verbose_name="Description",
        help_text="Описание товара или услуги.",
    )
    price: models.Field = models.PositiveIntegerField(
        verbose_name="Price",
        help_text="Цена товара или услуги.",
    )
    created_at: models.Field = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of creation",
        help_text="Дата и время создания объявления.",
    )
    author: models.Field = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Author",
        help_text="Создатель объявления.",
        related_name="ads",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"
        ordering = ("created_at",)


class Comment(models.Model):
    """Модель сущности отзыва/коментария"""

    text: models.Field = models.TextField(
        verbose_name="Text",
        help_text="Содержание отзыва.",
    )
    author: models.Field = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Author",
        help_text="Автор отзыва.",
        related_name="comments",
    )
    ad: models.Field = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="Advertisement",
        help_text="Объявление, под которым оставлен отзыв.",
        related_name="ad_comments",
    )
    created_at: models.Field = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of creation",
        help_text="Дата и время создания отзыва.",
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ("created_at",)
