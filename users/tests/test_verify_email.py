import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_verify_email_get(unauthorized_client, waiting_confirm_register, user):
    """Тест верификации email при регистрации, метод get"""
    verify_url = reverse("users:verify-email", args=[waiting_confirm_register.id])
    token = waiting_confirm_register.token
    response = unauthorized_client.get(verify_url + f"?token={token}")
    user.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert user.is_active


@pytest.mark.django_db
def test_verify_email_post(unauthorized_client, waiting_confirm_register, user):
    """Тест верификации email при регистрации, метод post"""
    verify_url = reverse("users:verify-email", args=[waiting_confirm_register.id])
    data = {"token": waiting_confirm_register.token}
    response = unauthorized_client.post(verify_url, data)
    user.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert user.is_active


@pytest.mark.django_db
def test_verify_new_email(unauthorized_client, waiting_confirm_new_email, user):
    """Тест верификации email при смене"""
    verify_url = reverse("users:verify-email", args=[waiting_confirm_new_email.id])
    data = {"token": waiting_confirm_new_email.token}
    response = unauthorized_client.post(verify_url, data)
    user.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert user.email == waiting_confirm_new_email.new_email


@pytest.mark.django_db
def test_verify_bad_token(unauthorized_client, waiting_confirm_register, user, bad_token):
    """Тест защиты от подмены токена"""
    verify_url = reverse("users:verify-email", args=[waiting_confirm_register.id])
    data = {"token": bad_token}
    response = unauthorized_client.post(verify_url, data)
    user.refresh_from_db()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("error") == "This is not your token."
    assert not user.is_active
