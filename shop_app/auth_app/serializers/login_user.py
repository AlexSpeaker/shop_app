from typing import Any, Dict

from rest_framework import serializers
from utils import PasswordValidator


class LoginUserSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Класс-сериализатор для аутентификации пользователя.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            PasswordValidator(),
        ],
    )
    username = serializers.CharField(required=True, min_length=4, max_length=50)
