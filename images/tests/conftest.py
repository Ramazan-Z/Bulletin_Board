import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from board.models import Advertisement
from images.models import Image
from users.models import User


@pytest.fixture
def images_list_url():
    """URL списка изображений"""
    return reverse("images:images-list")


@pytest.fixture
def user():
    """Пользователь"""
    return User.objects.create_user(email="user@test.com", username="user", password="password")


@pytest.fixture
def other_user():
    """Другой пользователь"""
    return User.objects.create_user(email="other_user@test.com", username="other_user", password="password")


@pytest.fixture
def admin_user():
    """Администратор"""
    return User.objects.create_user(email="admin@test.com", username="admin", password="password", role="admin")


@pytest.fixture
def unauthorized_client():
    """Неавторизованный клиент"""
    return APIClient()


@pytest.fixture
def user_client(user):
    """Авторизованный клиент"""
    user_client = APIClient()
    user_client.force_authenticate(user=user)
    return user_client


@pytest.fixture
def admin_client(admin_user):
    """Клиент авторизованный как администратор"""
    admin_client = APIClient()
    admin_client.force_authenticate(user=admin_user)
    return admin_client


@pytest.fixture
def ad_user(user):
    """Объявление пользователя"""
    return Advertisement.objects.create(title="Test users ad", description="Test description", price=1000, author=user)


@pytest.fixture
def ad_other_user(other_user):
    """Объявление другого пользователя"""
    return Advertisement.objects.create(
        title="Test other users ad", description="Test description", price=2000, author=other_user
    )


@pytest.fixture
def image_ad_user(ad_user):
    """Изображение объявления пользователя"""
    # with open("images/tests/test_image.png", "rb") as file:
    #    img = file.read()
    return Image.objects.create(ad=ad_user, image="images/tests/test_image.png")


@pytest.fixture
def image_ad_other_user(ad_other_user):
    """Изображение объявления другого пользователя"""
    # with open("images/tests/test_image.png", "rb") as file:
    #    img = file.read()
    return Image.objects.create(ad=ad_other_user, image="images/tests/test_image.png")
