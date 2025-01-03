from auth_app.serializers.login_user import LoginUserSerializer
from django.contrib.auth import authenticate, login
from drf_spectacular.utils import OpenApiResponse, extend_schema
from order_app.api_views.utils import merge_baskets, order_anonymous_to_user
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import get_user_data


class UserLoginAPIView(APIView):
    """
    Класс аутентификации пользователя.
    """

    serializer_class = LoginUserSerializer

    @extend_schema(
        request=LoginUserSerializer,
        responses={
            200: OpenApiResponse(description="Успешная аутентификация пользователя."),
            400: OpenApiResponse(description="Ошибка аутентификации пользователя."),
        },
        description="Аутентификация пользователя.",
        tags=("Auth",),
    )
    def post(self, request: Request) -> Response:
        """
        Post запрос аутентификации пользователя.
        Проверит существование пользователя и переданный пароль,
        если всё хорошо - выполнит вход.

        :param request: Request.
        :return: Response.
        """
        user_data = get_user_data(request.data)
        user_serializer = self.serializer_class(data=user_data)
        if not user_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=user_serializer.validated_data["username"],
            password=user_serializer.validated_data["password"],
        )
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        merge_baskets(user, request)
        order_anonymous_to_user(user, request)
        return Response(status=status.HTTP_200_OK)
