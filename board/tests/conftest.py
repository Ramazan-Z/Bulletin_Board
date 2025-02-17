import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from board.models import Advertisement, Comment
from users.models import User


@pytest.fixture
def list_ads_url():
    """URL списка объявлений"""
    return reverse("board:ads")


@pytest.fixture
def list_comment_url():
    """URL списка отзывов"""
    return reverse("board:comments")


@pytest.fixture
def create_ad_url():
    """URL создания объявлений"""
    return reverse("board:create_ad")


@pytest.fixture
def create_comment_url():
    """URL создания отзыва"""
    return reverse("board:create_comments")


@pytest.fixture
def new_ad_data():
    """Данные обновления объявления"""
    return {"title": "New title", "description": "New description", "price": 900}


@pytest.fixture
def user():
    """Пользователь"""
    return User.objects.create_user(email="user@test.com", username="user", password="password")


@pytest.fixture
def other_user():
    """Другой пользователь"""
    return User.objects.create_user(email="other_user@test.com", username="other_user", password="password")


@pytest.fixture
def third_user():
    """Третий пользователь"""
    return User.objects.create_user(email="third_user@test.com", username="third_user", password="password")


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
def comment_user(user, ad_other_user):
    """Отзыв пользователя"""
    return Comment.objects.create(text="Test users comment", ad=ad_other_user, author=user)


@pytest.fixture
def comment_other_user(other_user, ad_user):
    """Отзыв другого пользователя"""
    return Comment.objects.create(text="Test  other users comment", ad=ad_user, author=other_user)


@pytest.fixture
def new_comment_data(ad_user):
    """Данные обновления отзыва"""
    return {"text": "New text", "ad": ad_user.pk}
