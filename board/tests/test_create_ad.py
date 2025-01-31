import pytest
from rest_framework import status

from board.models import Advertisement


@pytest.mark.django_db
def test_authorized_error(unauthorized_client, create_ad_url):
    """Тест ошибки авторизации"""
    response = unauthorized_client.post(create_ad_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_validations_error(user_client, create_ad_url):
    """Тест отсутствия обязательных полей"""
    data = {}
    response = user_client.post(create_ad_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "title" in response.json()
    assert "description" in response.json()
    assert "price" in response.json()
    assert Advertisement.objects.all().count() == 0


@pytest.mark.django_db
def test_success_create_ad(user_client, create_ad_url, user):
    """Тест успешного создания объявления"""
    data = {"title": "Test ad", "description": "Test description", "price": 500}
    response = user_client.post(create_ad_url, data)
    ad = Advertisement.objects.get(id=response.json().get("id"))
    assert response.status_code == status.HTTP_201_CREATED
    assert Advertisement.objects.all().count() == 1
    assert ad.author == user
