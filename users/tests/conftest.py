import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User, WaitingConfirmEmail


@pytest.fixture
def register_url():
    """URL регистрации"""
    return reverse("users:user-register")


@pytest.fixture
def list_url():
    """URL списка пользователей"""
    return reverse("users:users-list")


@pytest.fixture
def reset_password_url():
    """URL сброса пароля"""
    return reverse("users:reset-password")


@pytest.fixture
def reset_password_confirm_url():
    """URL подтверждения сброса пароля"""
    return reverse("users:reset-password-confirm")


@pytest.fixture
def register_data():
    """Данные регистрации"""
    return {"email": "user@test.com", "username": "user", "password": "password"}


@pytest.fixture
def new_data():
    """Данные обновления профиля"""
    return {"email": "new_email@test.com", "username": "new_name", "password": "new_password"}


@pytest.fixture
def user(register_data):
    """Пользователь"""
    return User.objects.create_user(**register_data)


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
def waiting_confirm_register(user):
    """Ожидание подтверждения почты при регистрации"""
    token = AccessToken.for_user(user)
    user.is_active = False
    user.save()
    waiting_confirm = WaitingConfirmEmail.objects.create(user=user, token=token)
    return waiting_confirm


@pytest.fixture
def waiting_confirm_new_email(user):
    """Ожидание подтверждения почты при смене"""
    token = AccessToken.for_user(user)
    new_email = "new_email@test.com"
    waiting_confirm = WaitingConfirmEmail.objects.create(user=user, token=token, new_email=new_email)
    return waiting_confirm


@pytest.fixture
def user_token(user):
    """Токен пользователя"""
    return AccessToken.for_user(user)


@pytest.fixture
def bad_token(other_user):
    """Чужой токен"""
    return AccessToken.for_user(other_user)
