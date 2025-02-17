import pytest
from rest_framework import status

from users.models import User


@pytest.mark.django_db
def test_authorized_error(unauthorized_client, list_url):
    """Тест ошибки авторизации"""
    response = unauthorized_client.get(list_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_not_have_permission(user_client, list_url):
    """Тест отказа в доступе"""
    response = user_client.get(list_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_success_get_list(admin_client, user, other_user, list_url):
    """Тест успешного просмотра списка"""
    response = admin_client.get(list_url + "?ordering=id")
    assert response.status_code == status.HTTP_200_OK
    assert user in User.objects.all()
    assert other_user in User.objects.all()
    assert response.json().get("count") == 3


@pytest.mark.django_db
def test_filter_list(admin_client, user, other_user, list_url):
    """Тест фильтрации списка"""
    response = admin_client.get(list_url + "?ordering=id&role=admin")
    assert response.status_code == status.HTTP_200_OK
    assert user in User.objects.all()
    assert other_user in User.objects.all()
    assert response.json().get("count") == 1
