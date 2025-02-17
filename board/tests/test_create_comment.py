import pytest
from rest_framework import status

from board.models import Comment


@pytest.mark.django_db
def test_authorized_error(unauthorized_client, create_comment_url):
    """Тест ошибки авторизации"""
    response = unauthorized_client.post(create_comment_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_validations_error(user_client, create_comment_url):
    """Тест отсутствия обязательных полей"""
    data = {}
    response = user_client.post(create_comment_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "text" in response.json()
    assert "ad" in response.json()
    assert Comment.objects.all().count() == 0


@pytest.mark.django_db
def test_success_create_comment(user_client, create_comment_url, ad_other_user, user):
    """Тест успешного создания отзыва"""
    data = {"text": "Test comment", "ad": ad_other_user.pk}
    response = user_client.post(create_comment_url, data)
    comment = Comment.objects.get(id=response.json().get("id"))
    assert response.status_code == status.HTTP_201_CREATED
    assert Comment.objects.all().count() == 1
    assert comment.author == user
