from typing import Dict

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer[User]):
    """
    Класс-сериализатор для модели User.
    """

    class Meta:
        model = User
        fields = ("password", "username", "first_name", "last_name")

    @staticmethod
    def validate_username(value: str) -> str:
        """
        Проверка уникальности имени пользователя.

        :param value: Введённый username.
        :return: Проверенный username.
        """
        if len(value) < 6:
            raise serializers.ValidationError("Логин должен быть не менее 6 символов.")
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Это имя пользователя уже занято.")
        return value

    @staticmethod
    def validate_first_name(value: str) -> str:
        """
        Проверка имени пользователя.

        :param value: Введённое имя.
        :return: Проверенное имя.
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Имя должно быть не менее 2-х символов.")
        return value

    @staticmethod
    def validate_password(value: str) -> str:
        """
        Проверка сложности пароля.

        :param value: Введённый пароль.
        :return: Проверенный пароль.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Пароль должен содержать не менее 8 символов."
            )
        return value

    def create(self, validated_data: Dict[str, str]) -> User:
        """
        Создание нового пользователя.

        :param validated_data: Проверенные данные пользователя.
        :return: User.
        """

        return User.objects.create_user(**validated_data)
