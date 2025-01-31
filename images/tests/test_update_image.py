import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_permission_error(user_client, image_ad_other_user):
    """Тест попытки редактирования чужого изображения"""
    update_url = reverse("images:images-detail", args=[image_ad_other_user.pk])
    response = user_client.patch(update_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_update_self_image(user_client, image_ad_user, ad_user):
    """Тест редактирования своего изображения"""
    update_url = reverse("images:images-detail", args=[image_ad_user.pk])
    with open("images/tests/test_image.png", "rb") as file:
        data = {"ad": ad_user.pk, "image": file}
        response = user_client.put(update_url, data, format="multipart")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("ad") == ad_user.pk
