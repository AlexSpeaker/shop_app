from django.contrib.auth import logout
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


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
        Выполнит logout для пользователя.

        :param request: Request.
        :return: Response.
        """
        user = request.user
        if user.is_authenticated:
            logout(request)
        return Response(status=status.HTTP_200_OK)
