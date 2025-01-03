from auth_app.serializers.password import ChangePasswordSerializer
from django.contrib.auth import login
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ChangePasswordAPIView(APIView):
    """
    Класс смены пароля пользователя.
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Успешная операция."),
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Смена пароля пользователя.",
        tags=("Profile",),
    )
    def post(self, request: Request) -> Response:
        """
        Пост запрос смены пароля.

        :param request: Request.
        :return: Response.
        """
        user = request.user
        if user.is_authenticated:
            user_serializer = self.serializer_class(data=request.data, instance=user)
            if user_serializer.is_valid():
                user_serializer.update(
                    instance=user, validated_data=user_serializer.validated_data
                )
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
