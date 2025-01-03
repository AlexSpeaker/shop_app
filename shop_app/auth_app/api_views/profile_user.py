from auth_app.serializers.profile import ProfileSerializer
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserProfileAPIView(APIView):
    """
    Класс профиля пользователя.
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    @extend_schema(
        request=None,
        responses={
            200: ProfileSerializer,
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Получение данных пользователя.",
        tags=("Profile",),
    )
    def get(self, request: Request) -> Response:
        """
        Получение профиля пользователя.

        :param request: Request.
        :return: Response.
        """
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_serializer = self.serializer_class(instance=request.user.profile)
        return Response(user_serializer.data)

    @extend_schema(
        request=ProfileSerializer,
        responses={
            200: ProfileSerializer,
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Обновление данных пользователя.",
        tags=("Profile",),
    )
    def post(self, request: Request) -> Response:
        """
        Обновление профиля пользователя.

        :param request: Request.
        :return: Response.
        """
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.update(
                validated_data=user_serializer.validated_data,
                instance=request.user.profile,
            )
            return Response(self.serializer_class(instance=request.user.profile).data)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
