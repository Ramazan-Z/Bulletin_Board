import pytest
from rest_framework import status

from board.models import Comment


@pytest.mark.django_db
def test_comments_list(user_client, list_comment_url, comment_user, comment_other_user):
    """Тест списка отзывов"""
    response = user_client.get(list_comment_url)
    assert response.status_code == status.HTTP_200_OK
    assert comment_user in Comment.objects.all()
    assert comment_other_user in Comment.objects.all()
    assert response.json().get("count") == 2


@pytest.mark.django_db
def test_search_comment(user_client, list_comment_url, comment_user, comment_other_user):
    """Тест поиска отзыва"""
    response = user_client.get(list_comment_url + f"?search={comment_other_user.text}")
    assert response.status_code == status.HTTP_200_OK
    assert comment_user in Comment.objects.all()
    assert comment_other_user in Comment.objects.all()
    assert response.json().get("count") == 1
    assert response.json()["results"][0]["text"] == str(comment_other_user)


@pytest.mark.django_db
def test_ordering_comments(user_client, list_comment_url, comment_user, comment_other_user):
    """Тест сортировки отзывов по дате"""
    response = user_client.get(list_comment_url + "?ordering=-created_at")
    results = response.json()["results"]
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("count") == 2
    assert comment_user in Comment.objects.all()
    assert comment_other_user in Comment.objects.all()
    assert results[0]["created_at"] > results[1]["created_at"]


@pytest.mark.django_db
def test_filter_author_comments(user_client, list_comment_url, comment_user, comment_other_user):
    """Тест фильтрации отзывов по авторам"""
    response = user_client.get(list_comment_url + f"?author={comment_user.author.pk}")
    assert response.status_code == status.HTTP_200_OK
    assert comment_user in Comment.objects.all()
    assert comment_other_user in Comment.objects.all()
    assert response.json().get("count") == 1
    assert response.json()["results"][0]["author"] == comment_user.author.pk
