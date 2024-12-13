from auth_app.views_api import (
    ChangePasswordAPIView,
    RegisterUserAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserProfileAPIView,
    UserProfileAvatarAPIView,
)
from django.urls import path

urlpatterns = [
    path("sign-up", RegisterUserAPIView.as_view(), name="registration"),
    path("sign-in", UserLoginAPIView.as_view(), name="login"),
    path("sign-out", UserLogoutAPIView.as_view(), name="logout"),
    path("profile", UserProfileAPIView.as_view(), name="profile"),
    path("profile/avatar", UserProfileAvatarAPIView.as_view(), name="profile_avatar"),
    path("profile/password", ChangePasswordAPIView.as_view(), name="profile_password"),
]
