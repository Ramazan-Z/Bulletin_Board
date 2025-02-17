import pytest
from rest_framework import status

from images.models import Image


@pytest.mark.django_db
def test_authorized_error(unauthorized_client, images_list_url):
    """Тест ошибки авторизации"""
    response = unauthorized_client.post(images_list_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_validations_error(user_client, images_list_url, ad_other_user):
    """Тест попытки добавить изображение к чужому объявлению"""
    with open("images/tests/test_image.png", "rb") as file:
        data = {"ad": ad_other_user.pk, "image": file}
        response = user_client.post(images_list_url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("non_field_errors") == ["Specify your ad."]


@pytest.mark.django_db
def test_success_add_image(user_client, images_list_url, ad_user):
    """Тест успешного добавления изображения"""
    with open("images/tests/test_image.png", "rb") as file:
        data = {"ad": ad_user.pk, "image": file}
        response = user_client.post(images_list_url, data, format="multipart")
    img = Image.objects.get(pk=response.json().get("id"))
    assert response.status_code == status.HTTP_201_CREATED
    assert Image.objects.all().count() == 1
    assert str(img) == str(ad_user)
