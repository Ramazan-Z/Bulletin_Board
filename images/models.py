from django.db import models

from board.models import Advertisement


class Image(models.Model):
    """Модель изображения товара"""

    image: models.Field = models.ImageField(
        upload_to="images/",
        verbose_name="Image",
        help_text="Графический файл (фотография товара).",
    )
    ad: models.Field = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="Advertisement",
        help_text="Объявление, связанное с этим изображением.",
        related_name="images",
    )

    def __str__(self):
        return str(self.ad)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
