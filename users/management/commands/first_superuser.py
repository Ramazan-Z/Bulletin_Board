import os

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание суперпользователя."

    def handle(self, *args, **options):
        User.objects.create_user(
            email=os.getenv("SUPERUSER_EMAIL", "superuser@sky.pro"),
            username=os.getenv("SUPERUSER_USERNAME", "superuser"),
            password=os.getenv("SUPERUSER_PASSWORD", "superuser"),
            is_staff=True,
            is_superuser=True,
        )
        self.stdout.write(self.style.SUCCESS("Successfully created superuser."))
