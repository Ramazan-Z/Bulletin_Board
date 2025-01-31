import pytest
from django.urls import reverse
from rest_framework import status

from images.models import Image


@pytest.mark.django_db
def test_permission_error(user_client, image_ad_other_user):
    """Тест попытки удаления чужого изображения"""
    delete_url = reverse("images:images-detail", args=[image_ad_other_user.pk])
    response = user_client.delete(delete_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_delete_self_image(user_client, image_ad_user):
    """Тест удаления своего изображения"""
    delete_url = reverse("images:images-detail", args=[image_ad_user.pk])
    response = user_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Image.objects.all().count() == 0


@pytest.mark.django_db
def test_delete_admin(admin_client, image_ad_user):
    """Тест удаления чужого изображения администратором"""
    delete_url = reverse("images:images-detail", args=[image_ad_user.pk])
    response = admin_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Image.objects.all().count() == 0
