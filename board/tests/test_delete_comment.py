import pytest
from django.urls import reverse
from rest_framework import status

from board.models import Comment


@pytest.mark.django_db
def test_permission_error(user_client, comment_other_user):
    """Тест попытки удaления чужого отзыва"""
    delete_url = reverse("board:delete_comments", args=[comment_other_user.pk])
    response = user_client.delete(delete_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_delete_self_comment(user_client, comment_user):
    """Тест удаления своего отзыва"""
    delete_url = reverse("board:delete_comments", args=[comment_user.pk])
    response = user_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.all().count() == 0


@pytest.mark.django_db
def test_delete_admin(admin_client, comment_user):
    """Тест удаления чужого отзыва администратором"""
    delete_url = reverse("board:delete_comments", args=[comment_user.pk])
    response = admin_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.all().count() == 0
