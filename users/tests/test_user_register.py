from unittest.mock import Mock

import pytest
from rest_framework import status

from users.models import User, WaitingConfirmEmail
from users.services import send_email_info


@pytest.mark.django_db
def test_success_register(unauthorized_client, register_url, register_data):
    """Тест успешной регистрации"""
    mock_send_email_info = Mock(return_value=None)
    send_email_info.delay = mock_send_email_info

    response = unauthorized_client.post(register_url, register_data)

    mock_send_email_info.assert_called_once()
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.all().count() == 1
    assert WaitingConfirmEmail.objects.all().count() == 1
    assert not User.objects.get(id=response.json().get("id")).is_active


@pytest.mark.django_db
def test_already_exists(unauthorized_client, register_url, register_data, user):
    """Тест регистрации уже существующих данных"""
    response = unauthorized_client.post(register_url, register_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.all().count() == 1
    assert WaitingConfirmEmail.objects.all().count() == 0
    assert user.is_active


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data",
    [
        ({"username": "user", "password": "password"}),  # no email
        ({"email": "user@test.com", "password": "password"}),  # no username
        ({"email": "user@test.com", "username": "user"}),  # no password
        ({"email": "@test.com", "username": "user", "password": "password"}),  # bad email
        ({"email": "user@test.com", "username": "user", "password": "password", "phone": "qwerty"}),  # bad phone
        ({"email": "user@test.com", "username": "user", "password": "password", "phone": "12345"}),  # bad phone
    ],
)
def test_validator_error(data, unauthorized_client, register_url):
    """Тест регистрации c ошибкой валидации"""
    response = unauthorized_client.post(register_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.all().count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "phone_number",
    [
        ("89999999999",),
        ("8 999 999 99 99",),
        ("8-999-999-99-99",),
        ("+7(999)999 99 99",),
        ("+7(999)999-99-99",),
        ("8(999)9999999",),
    ],
)
def test_phone_normalize(phone_number, unauthorized_client, register_url, register_data):
    """Тест нормализатора номера телефона"""
    mock_send_email_info = Mock(return_value=None)
    send_email_info.delay = mock_send_email_info

    register_data["phone"] = phone_number
    response = unauthorized_client.post(register_url, register_data)

    mock_send_email_info.assert_called_once()
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("phone") == "+7(999)999-99-99"
