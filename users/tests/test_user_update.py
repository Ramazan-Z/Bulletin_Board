from unittest.mock import Mock

import pytest
from django.urls import reverse
from rest_framework import status

from users.models import WaitingConfirmEmail
from users.services import send_email_info


@pytest.mark.django_db
def test_authorized_error(unauthorized_client, new_data, user):
    """Тест ошибки авторизации"""
    update_url = reverse("users:user-update", args=[user.pk])
    response = unauthorized_client.patch(update_url, new_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_other_profile_update(user_client, new_data, other_user):
    """Тест попытки обновления чужого профиля"""
    update_url = reverse("users:user-update", args=[other_user.pk])
    response = user_client.put(update_url, new_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_self_profile_update(user_client, new_data, user):
    """Тест обновления своего профиля"""
    mock_send_email_info = Mock(return_value=None)
    send_email_info.delay = mock_send_email_info

    update_url = reverse("users:user-update", args=[user.pk])
    last_email = user.email
    response = user_client.put(update_url, new_data)
    user.refresh_from_db()
    waiting_confirm = WaitingConfirmEmail.objects.get(user=user)

    mock_send_email_info.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    assert user.check_password(new_data.get("password"))
    assert user.email == last_email
    assert waiting_confirm.new_email == new_data.get("email")
