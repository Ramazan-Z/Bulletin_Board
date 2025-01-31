import pytest
from django.urls import reverse
from rest_framework import status

from board.models import Advertisement


@pytest.mark.django_db
def test_permission_error(user_client, ad_other_user):
    """Тест попытки удаления чужого объявления"""
    delete_url = reverse("board:delete_ad", args=[ad_other_user.pk])
    response = user_client.delete(delete_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_delete_self_ad(user_client, ad_user):
    """Тест удаления своего объявления"""
    delete_url = reverse("board:delete_ad", args=[ad_user.pk])
    response = user_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Advertisement.objects.all().count() == 0


@pytest.mark.django_db
def test_delete_admin(admin_client, ad_user):
    """Тест удаления чужого объявления администратором"""
    delete_url = reverse("board:delete_ad", args=[ad_user.pk])
    response = admin_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Advertisement.objects.all().count() == 0
