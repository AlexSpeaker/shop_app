from typing import Any, Dict, Optional

from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db.models.fields.files import ImageFieldFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Profile
from .utils import PhoneValidator


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


class AvatarSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Класс-сериализатор для аватарки пользователя.
    """
    src = serializers.CharField(default=None, allow_null=True)
    alt = serializers.CharField(default="No Image")

    @staticmethod
    def get_src(instance: Any) -> Optional[str]:
        """
        Функция проверит, является ли объект ImageFieldFile и вернёт либо путь к картинке, либо None.

        :param instance: Объект.
        :return: Если объект ImageFieldFile, то вернёт путь к картинке, иначе None.
        """
        return instance.url if isinstance(instance, ImageFieldFile) else None


class ProfileSerializer(serializers.ModelSerializer[Profile]):
    """
    Класс-сериализатор для профиля пользователя.
    """
    fullName = serializers.CharField(min_length=2, max_length=150, required=True)
    email = serializers.CharField(required=False, validators=[EmailValidator()])
    phone = serializers.CharField(required=False, validators=[PhoneValidator()])
    avatar = AvatarSerializer(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

    @staticmethod
    def validate_avatar(image: Any) -> Optional[ImageFieldFile]:
        """
        Функция проверит входящий объект. Ожидаем ImageFieldFile.

        :param image: Объект.
        :return: Если объект не ImageFieldFile, то вернёт None.
            Если ImageFieldFile, то проверит размер и вернёт ImageFieldFile.
        """
        if not isinstance(image, ImageFieldFile):
            return None
        max_file_size = 1000000
        if image.size > max_file_size:
            raise ValidationError(f"Файл слишком большой! Допустимый размер: {max_file_size} Б.")
        return image
