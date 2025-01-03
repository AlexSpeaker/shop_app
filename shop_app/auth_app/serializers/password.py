from typing import Any, Dict

from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers
from utils import PasswordValidator


class ChangePasswordSerializer(serializers.Serializer[AbstractBaseUser]):
    """
    Класс-сериализатор для смены пароля пользователя.
    """

    currentPassword = serializers.CharField(
        write_only=True, required=True, validators=[PasswordValidator()]
    )
    newPassword = serializers.CharField(
        write_only=True, required=True, validators=[PasswordValidator()]
    )

    def validate_currentPassword(self, value: str) -> str:
        """
        Проверяем текущий пароль.

        :param value: Пароль.
        :return: Пароль.
        """
        if self.instance is None:
            raise serializers.ValidationError("Нет переданного пользователя.")
        if not self.instance.check_password(value):
            raise serializers.ValidationError("Не верный пароль.")
        return value

    def update(
        self, instance: AbstractBaseUser, validated_data: Dict[str, Any]
    ) -> AbstractBaseUser:
        """
        Обновляем пароль пользователю.

        :param instance: Пользователь.
        :param validated_data: Проверенные данные.
        :return: Пользователь.
        """
        instance.set_password(validated_data["newPassword"])
        instance.save()
        return instance
