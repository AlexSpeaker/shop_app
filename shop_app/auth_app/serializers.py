from typing import Any, Dict

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class RegisterUserSerializer(serializers.ModelSerializer[User]):
    """
    Класс-сериализатор для регистрации пользователя.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=50,
        style={"input_type": "password"},
        required=True,
    )
    name = serializers.CharField(
        required=True, min_length=2, max_length=50, write_only=True
    )
    username = serializers.CharField(required=True, min_length=4, max_length=50)

    class Meta:
        model = User
        fields = ["username", "password", "name"]

    @staticmethod
    def validate_username(value: str) -> str:
        """
        Проверка уникальности имени пользователя.

        :param value: Введённый username.
        :return: Проверенный username.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Это имя пользователя уже занято.")
        return value

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Функция создаст пользователя и его профиль.

        :param validated_data: Валидные данные.
        :return: Созданный пользователь.
        """
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        Profile.objects.create(name=validated_data["name"], user=user)
        return user


class LoginUserSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Класс-сериализатор для аутентификации пользователя.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=50,
        style={"input_type": "password"},
        required=True,
    )
    username = serializers.CharField(required=True, min_length=4, max_length=50)
