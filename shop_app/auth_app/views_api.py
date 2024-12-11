from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.serializers import LoginUserSerializer, RegisterUserSerializer
from auth_app.utils import get_user_data


class RegisterUserAPIView(APIView):
    """
    Класс регистрации пользователя.
    """

    serializer_class = RegisterUserSerializer

    @extend_schema(
        request=RegisterUserSerializer,
        responses={
            200: OpenApiResponse(description="Успешная регистрация пользователя."),
            500: OpenApiResponse(description="Ошибка регистрации пользователя."),
        },
        description="Создание нового пользователя.",
        tags=("Auth",),
    )
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
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user = user_serializer.create(user_data)
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    """
    Класс аутентификации пользователя.
    """

    serializer_class = LoginUserSerializer

    @extend_schema(
        request=LoginUserSerializer,
        responses={
            200: OpenApiResponse(description="Успешная аутентификация пользователя."),
            500: OpenApiResponse(description="Ошибка аутентификации пользователя."),
        },
        description="Аутентификация пользователя.",
        tags=("Auth",),
    )
    def post(self, request: Request) -> Response:
        """
        Post запрос аутентификации пользователя.
        Проверит существование пользователя и переданный пароль,
        если всё хорошо - выполнит вход.
        Иначе - вернёт ошибку 500.

        :param request: Request.
        :return: Response.
        """
        user_data = get_user_data(request.data)
        user_serializer = self.serializer_class(data=user_data)
        if not user_serializer.is_valid():
            return Response(
                user_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        user = authenticate(
            username=user_serializer.validated_data["username"],
            password=user_serializer.validated_data["password"],
        )
        if not user:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class UserLogoutAPIView(APIView):
    """
    Класс выхода пользователя из системы.
    """

    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(description="Успешная операция."),
        },
        description="Выход пользователя из системы.",
        tags=("Auth",),
    )
    def post(request: Request) -> Response:
        """
        Выполнит logout для пользователя,
        если он был до этого аутентифицирован в системе.

        :param request: Request.
        :return: Response.
        """
        user = request.user
        if user.is_authenticated:
            logout(request)
        return Response(status=status.HTTP_200_OK)
