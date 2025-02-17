from django.urls import path

from board import apps, views

app_name = apps.BoardConfig.name

urlpatterns = [
    # Advertisements
    path("ads/", views.ListAdsView.as_view(), name="ads"),
    path("create_ad/", views.CreateAdView.as_view(), name="create_ad"),
    path("retrieve_ad/<int:pk>/", views.RetrieveAdView.as_view(), name="retrieve_ad"),
    path("update_ad/<int:pk>/", views.UpdateAdView.as_view(), name="update_ad"),
    path("delete_ad/<int:pk>/", views.DestroyAdView.as_view(), name="delete_ad"),
    # Comments
    path("comments/", views.ListComments.as_view(), name="comments"),
    path("create_comments/", views.CreateComment.as_view(), name="create_comments"),
    path("retrieve_comments/<int:pk>/", views.RetrieveComment.as_view(), name="retrieve_comments"),
    path("update_comments/<int:pk>/", views.UpdateComment.as_view(), name="update_comments"),
    path("delete_comments/<int:pk>/", views.DestroyComment.as_view(), name="delete_comments"),
    # Contact between seller and buyer
    path("send_message/<int:user_id>/<int:ad_id>/", views.SendMessage.as_view(), name="send_message"),
]
