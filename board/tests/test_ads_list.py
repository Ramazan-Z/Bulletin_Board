import pytest
from rest_framework import status

from board.models import Advertisement


@pytest.mark.django_db
def test_ads_list(unauthorized_client, list_ads_url, ad_user, ad_other_user):
    """Тест списка объявлений"""
    response = unauthorized_client.get(list_ads_url)
    assert response.status_code == status.HTTP_200_OK
    assert ad_user in Advertisement.objects.all()
    assert ad_other_user in Advertisement.objects.all()
    assert response.json().get("count") == 2


@pytest.mark.django_db
def test_search_ads(unauthorized_client, list_ads_url, ad_user, ad_other_user):
    """Тест поиска объявлений"""
    response = unauthorized_client.get(list_ads_url + f"?search={ad_other_user.title}")
    assert response.status_code == status.HTTP_200_OK
    assert ad_user in Advertisement.objects.all()
    assert ad_other_user in Advertisement.objects.all()
    assert response.json().get("count") == 1
    assert response.json()["results"][0]["title"] == str(ad_other_user)


@pytest.mark.django_db
def test_ordering_ads(unauthorized_client, list_ads_url, ad_user, ad_other_user):
    """Тест сортировки объявлений"""
    response = unauthorized_client.get(list_ads_url + "?ordering=-price")
    results = response.json()["results"]
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("count") == 2
    assert results[0]["price"] == ad_other_user.price
    assert results[1]["price"] == ad_user.price
    assert results[0]["price"] > results[1]["price"]


@pytest.mark.django_db
def test_filter_price_ads(unauthorized_client, list_ads_url, ad_user, ad_other_user):
    """Тест фильтрации объявлений по цене"""
    response = unauthorized_client.get(list_ads_url + "?price_max=1500")
    assert response.status_code == status.HTTP_200_OK
    assert ad_user in Advertisement.objects.all()
    assert ad_other_user in Advertisement.objects.all()
    assert response.json().get("count") == 1
    assert response.json()["results"][0]["id"] == ad_user.pk
