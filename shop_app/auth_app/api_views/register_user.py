from auth_app.serializers.register_user import RegisterUserSerializer
from django.contrib.auth import login
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import get_user_data


class RegisterUserAPIView(APIView):
    """
    Класс регистрации пользователя.
    """

    serializer_class = RegisterUserSerializer

    @extend_schema(
        request=RegisterUserSerializer,
        responses={
            200: OpenApiResponse(description="Успешная регистрация пользователя."),
            400: OpenApiResponse(description="Ошибка регистрации пользователя."),
        },
        description="Создание нового пользователя.",
        tags=("Auth",),
    )
    def post(self, request: Request) -> Response:
        """
        Post запрос регистрации пользователя.
        Проверит входящие данные,
        и если всё хорошо - зарегистрирует пользователя и выполнит вход.

        :param request: Request.
        :return: Response.
        """

        user_data = get_user_data(request.data)
        user_serializer = self.serializer_class(data=user_data)
        if not user_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = user_serializer.create(user_serializer.validated_data)
        login(request, user)
        return Response(status=status.HTTP_200_OK)
