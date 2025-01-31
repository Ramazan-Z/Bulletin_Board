import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_permission_error(user_client, ad_other_user, new_ad_data):
    """Тест попытки редактирования чужого объявления"""
    update_url = reverse("board:update_ad", args=[ad_other_user.pk])
    response = user_client.patch(update_url, new_ad_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_update_self_ad(user_client, ad_user, new_ad_data):
    """Тест редактирования своего объявления"""
    update_url = reverse("board:update_ad", args=[ad_user.pk])
    response = user_client.put(update_url, new_ad_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("title") == new_ad_data["title"]
    assert response.json().get("description") == new_ad_data["description"]
    assert response.json().get("price") == new_ad_data["price"]


@pytest.mark.django_db
def test_update_admin(admin_client, ad_user, new_ad_data):
    """Тест редактирования чужого объявления администратором"""
    update_url = reverse("board:update_ad", args=[ad_user.pk])
    response = admin_client.put(update_url, new_ad_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("title") == new_ad_data["title"]
    assert response.json().get("description") == new_ad_data["description"]
    assert response.json().get("price") == new_ad_data["price"]
