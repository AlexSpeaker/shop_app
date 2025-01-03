from auth_app.api_views.avatar_user import UserProfileAvatarAPIView
from auth_app.api_views.login_user import UserLoginAPIView
from auth_app.api_views.logout_user import UserLogoutAPIView
from auth_app.api_views.password_user import ChangePasswordAPIView
from auth_app.api_views.profile_user import UserProfileAPIView
from auth_app.api_views.register_user import RegisterUserAPIView
from django.urls import path

app_name = "auth_app"
urlpatterns = [
    path("sign-up", RegisterUserAPIView.as_view(), name="registration"),
    path("sign-in", UserLoginAPIView.as_view(), name="login"),
    path("sign-out", UserLogoutAPIView.as_view(), name="logout"),
    path("profile", UserProfileAPIView.as_view(), name="profile"),
    path("profile/avatar", UserProfileAvatarAPIView.as_view(), name="profile_avatar"),
    path("profile/password", ChangePasswordAPIView.as_view(), name="profile_password"),
]
