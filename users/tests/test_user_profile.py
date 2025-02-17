import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_authorized_error(unauthorized_client, user):
    """Тест ошибки авторизации"""
    profile_url = reverse("users:user-profile", args=[user.pk])
    response = unauthorized_client.get(profile_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_self_profile_view(user_client, user):
    """Тест просмотра своего профиля"""
    profile_url = reverse("users:user-profile", args=[user.pk])
    response = user_client.get(profile_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == user.pk


@pytest.mark.django_db
def test_other_profile_view(user_client, other_user):
    """Тест просмотра чужого профиля"""
    profile_url = reverse("users:user-profile", args=[other_user.pk])
    response = user_client.get(profile_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_admin_profile_view(admin_client, user):
    """Тест просмотра чужого профиля администратором"""
    profile_url = reverse("users:user-profile", args=[user.pk])
    response = admin_client.get(profile_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == user.pk
