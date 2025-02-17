import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_authorized_error(unauthorized_client, ad_user):
    """Тест ошибки авторизации"""
    retrieve_url = reverse("board:retrieve_ad", args=[ad_user.pk])
    response = unauthorized_client.get(retrieve_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_retrieve_ad(user_client, ad_other_user):
    """Тест просмотра чужого объявления"""
    retrieve_url = reverse("board:retrieve_ad", args=[ad_other_user.pk])
    response = user_client.get(retrieve_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == ad_other_user.pk
