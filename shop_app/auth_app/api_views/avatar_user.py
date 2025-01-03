from auth_app.serializers.avatar import InAvatarSerializer
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserProfileAvatarAPIView(APIView):
    """
    Класс аватарки пользователя.
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InAvatarSerializer

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(description="Успешная операция."),
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Обновление аватарки пользователя. Принимает файл аватарки (data name - avatar).",
        tags=("Profile",),
    )
    def post(self, request: Request) -> Response:
        """
        Обновление аватарки пользователя.

        :param request: Request.
        :return: Response.
        """
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.update(
                instance=request.user.profile,
                validated_data=user_serializer.validated_data,
            )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
