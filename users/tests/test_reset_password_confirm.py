import pytest
from rest_framework import status

from users.models import WaitingConfirmEmail


@pytest.mark.django_db
def test_success_reset_password(unauthorized_client, user, user_token, reset_password_confirm_url):
    """Тест успешного сброса пароля"""
    data = {"user_id": user.pk, "token": user_token, "new_password": "new_password"}
    response = unauthorized_client.post(reset_password_confirm_url, data)
    user.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("result") == "Password changed successfully"
    assert user.check_password(data.get("new_password"))


@pytest.mark.django_db
def test_waiting_confirm_delete(
    unauthorized_client, user, user_token, reset_password_confirm_url, waiting_confirm_register
):
    """Тест удаления ожидания подтверждений при активации через сброс пароля"""
    data = {"user_id": user.pk, "token": user_token, "new_password": "new_password"}
    assert str(user.waitings) == str(waiting_confirm_register)
    response = unauthorized_client.post(reset_password_confirm_url, data)
    assert response.status_code == status.HTTP_200_OK
    assert not WaitingConfirmEmail.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_bad_token_protect(unauthorized_client, user, bad_token, reset_password_confirm_url, register_data):
    """Тест защиты от подмены токена"""
    data = {"user_id": user.pk, "token": bad_token, "new_password": "new_password"}
    response = unauthorized_client.post(reset_password_confirm_url, data)
    user.refresh_from_db()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("error") == "This is not your token."
    assert user.check_password(register_data.get("password"))
