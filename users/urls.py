from django.urls import path

from users import apps, views

app_name = apps.UsersConfig.name

urlpatterns = [
    path("list/", views.UsersList.as_view(), name="users-list"),
    path("register/", views.UserRegister.as_view(), name="user-register"),
    path("profile/<int:pk>/", views.UserProfile.as_view(), name="user-profile"),
    path("update/<int:pk>/", views.UserUpdate.as_view(), name="user-update"),
    path("delete/<int:pk>/", views.UserDestroy.as_view(), name="user-delete"),
    path("login/", views.UserLogin.as_view(), name="user-login"),
    path("refresh_token/", views.TokenRefresh.as_view(), name="refresh-token"),
    path("verify_email/<int:pk>/", views.VerifyEmail.as_view(), name="verify-email"),
    path("reset_password/", views.ResetPassword.as_view(), name="reset-password"),
    path("reset_password/confirm/", views.ResetPasswordConfirm.as_view(), name="reset-password-confirm"),
    path("admin_management/<int:pk>/", views.AdminManagement.as_view(), name="admin-management"),
]
