import pytest
from rest_framework import status

from images.models import Image


@pytest.mark.django_db
def test_filter_images_ad(user_client, images_list_url, image_ad_user, image_ad_other_user, ad_user):
    """Тест фильтрации изображений по объявлениям"""
    response = user_client.get(images_list_url + f"?ad={ad_user.pk}&ordering=ad")
    assert response.status_code == status.HTTP_200_OK
    assert image_ad_user in Image.objects.all()
    assert image_ad_other_user in Image.objects.all()
    assert response.json().get("count") == 1
    assert response.json()["results"][0]["id"] == image_ad_user.pk
