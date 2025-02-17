from unittest.mock import Mock

import pytest
from django.urls import reverse
from rest_framework import status

from board.services import send_email_info


@pytest.mark.django_db
def test_authorized_error(unauthorized_client, user, ad_user):
    """Тест ошибки авторизации"""
    send_url = reverse("board:send_message", args=[user.pk, ad_user.pk])
    response = unauthorized_client.post(send_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_success_send_msg(user_client, other_user, ad_other_user):
    """Тест успешной отправки сообщения"""
    mock_send_email_info = Mock(return_value=None)
    send_email_info.delay = mock_send_email_info

    send_url = reverse("board:send_message", args=[other_user.pk, ad_other_user.pk])
    data = {"message": "Test message"}
    response = user_client.post(send_url, data)

    mock_send_email_info.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("result") == "Your message has been sent."


@pytest.mark.django_db
def test_self_msg_error(user_client, user, ad_user):
    """Тест попытки отправить сообщение самому себе"""
    send_url = reverse("board:send_message", args=[user.pk, ad_user.pk])
    data = {"message": "Test message"}
    response = user_client.post(send_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("non_field_errors") == ["There is no need to send a message to yourself."]


@pytest.mark.django_db
def test_third_user_error(user_client, third_user, ad_other_user):
    """Тест попытки обсуждения объявления третьего пользователя"""
    send_url = reverse("board:send_message", args=[third_user.pk, ad_other_user.pk])
    data = {"message": "Test message"}
    response = user_client.post(send_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("non_field_errors") == [
        "You can only discuss your own advertisement or the recipient's advertisement."
    ]
