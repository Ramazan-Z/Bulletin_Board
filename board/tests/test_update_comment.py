import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_permission_error(user_client, comment_other_user, new_comment_data):
    """Тест попытки редактирования чужого отзыва"""
    update_url = reverse("board:update_comments", args=[comment_other_user.pk])
    response = user_client.patch(update_url, new_comment_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_update_self_comment(user_client, comment_user, new_comment_data):
    """Тест редактирования своего отзыва"""
    update_url = reverse("board:update_comments", args=[comment_user.pk])
    response = user_client.put(update_url, new_comment_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("text") == new_comment_data["text"]
    assert response.json().get("ad") == new_comment_data["ad"]


@pytest.mark.django_db
def test_update_admin(admin_client, comment_user, new_comment_data):
    """Тест редактирования чужого отзыва администратором"""
    update_url = reverse("board:update_comments", args=[comment_user.pk])
    response = admin_client.put(update_url, new_comment_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("text") == new_comment_data["text"]
    assert response.json().get("ad") == new_comment_data["ad"]
