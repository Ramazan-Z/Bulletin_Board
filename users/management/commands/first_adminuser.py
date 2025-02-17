import os

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание администратора."

    def handle(self, *args, **options):
        User.objects.create_user(
            email=os.getenv("ADMIN_EMAIL", "admin@sky.pro"),
            username=os.getenv("ADMIN_USERNAME", "admin"),
            password=os.getenv("ADMIN_PASSWORD", "admin"),
            role="admin",
        )
        self.stdout.write(self.style.SUCCESS("Successfully created adminuser."))
