from unittest.mock import Mock

import pytest
from rest_framework import status

from users.services import send_email_info


@pytest.mark.django_db
def test_reset_password(unauthorized_client, user, reset_password_url):
    """Тест сброса пароля"""
    mock_send_email_info = Mock(return_value=None)
    send_email_info.delay = mock_send_email_info

    data = {"email": user.email}
    response = unauthorized_client.post(reset_password_url, data)

    mock_send_email_info.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("result") == "The link was sent to the specified email."


@pytest.mark.django_db
def test_reset_password_no_exists(unauthorized_client, reset_password_url):
    """Тест сброса пароля, при не существующем email"""
    data = {"email": "no_exists@mail.ru"}
    response = unauthorized_client.post(reset_password_url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "No User matches the given query."
