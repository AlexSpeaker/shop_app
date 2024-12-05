from auth_app.views_api import RegisterUserAPIView, UserLoginAPIView, UserLogoutAPIView
from django.urls import path

urlpatterns = [
    path("sign-up", RegisterUserAPIView.as_view(), name="registration"),
    path("sign-in", UserLoginAPIView.as_view(), name="login"),
    path("sign-out", UserLogoutAPIView.as_view(), name="logout"),
]