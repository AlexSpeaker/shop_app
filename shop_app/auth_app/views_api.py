from auth_app.serializers import UserSerializer
from auth_app.utils import get_user_data
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterUserAPIView(APIView):
    """
    Класс регистрации пользователя.
    """

    serializer_class = UserSerializer

    def post(self, request: Request) -> Response:
        """
        Post запрос регистрации пользователя.
        Проверит входящие данные,
        и если всё хорошо - зарегистрирует пользователя и выполнит вход.
        Иначе вернёт ошибку 500.

        :param request: Request.
        :return: Response.
        """

        user_data = get_user_data(request.data)
        user_serializer = self.serializer_class(data=user_data)
        if not user_serializer.is_valid():
            return Response(
                user_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        user = user_serializer.create(user_data)
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    """
    Класс аутентификации пользователя.
    """

    @staticmethod
    def post(request: Request) -> Response:
        """
        Post запрос аутентификации пользователя.
        Проверит существование пользователя и переданный пароль,
        если всё хорошо - выполнит вход.
        Иначе - вернёт ошибку 500.

        :param request: Request.
        :return: Response.
        """
        user_data = get_user_data(request.data)
        users = User.objects.filter(username=user_data.get("username", ""))
        if (
            users.count() == 1
            and users[0].check_password(user_data.get("password", ""))
            and users[0].is_active
        ):
            login(request, users[0])
            return Response(status=status.HTTP_200_OK)
        response = Response()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response


class UserLogoutAPIView(APIView):
    """
    Класс выхода пользователя из системы.
    """

    @staticmethod
    def post(request: Request) -> Response:
        """
        Post запрос аутентификации пользователя.
        Выполнит logout для пользователя,
        если он был до этого аутентифицирован в системе.

        :param request: Request.
        :return: Response.
        """
        user = request.user
        if user.is_authenticated:
            logout(request)
        return Response(status=status.HTTP_200_OK)
