from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import phone_number_validator


class User(AbstractUser):
    """Модель сущности пользователя."""

    ROLE_CHOICES = [
        ("user", "Пользователь сайта."),
        ("admin", "Администратор сайта."),
    ]

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Электронная почта пользователя.",
    )
    phone: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=16,
        verbose_name="Phone number",
        validators=[phone_number_validator],
        help_text=(
            "Номер телефона для связи. Разделители групп: пробел, тире или сплошной набор. "
            "Например: +7 XXX XXX XX XX; +7-XXX-XXX-XX-XX; 8(XXX)XXX XX XX; 8XXXXXXXXXX"
        ),
    )
    city: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        verbose_name="City",
        help_text="Город или населенный пункт.",
    )
    avatar: models.Field = models.ImageField(
        blank=True,
        null=True,
        upload_to="users/avatars/",
        verbose_name="Avatar",
        help_text="Графический файл (фотография).",
    )
    role: models.Field = models.CharField(
        max_length=5,
        choices=ROLE_CHOICES,
        default="user",
        verbose_name="The role of the site user",
        help_text="Назначается только администратором сайта.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class WaitingConfirmEmail(models.Model):
    """Модель ожидания подтверждения Email (Регистрация или смена)."""

    user: models.Field = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="Указывает пользователя, от которого ожидается подтверждение.",
        related_name="waitings",
    )
    new_email: models.Field = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="New email",
        help_text="Электронная почта, ожидающая подтверждение.",
    )
    token: models.Field = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Token",
        help_text="Секретный код подтверждения.",
    )

    def __str__(self):
        return f"Waiting confirm from {self.user}."

    class Meta:
        verbose_name = "Waiting for confirmation"
        verbose_name_plural = "Waitings for confirmation"
