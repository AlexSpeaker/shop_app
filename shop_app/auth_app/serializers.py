from typing import Any, Dict, Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db.models.fields.files import ImageFieldFile
from rest_framework import serializers

from .models import Profile
from .utils import PasswordValidator, PhoneValidator, delete_file


class RegisterUserSerializer(serializers.ModelSerializer[User]):
    """
    Класс-сериализатор для регистрации пользователя.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            PasswordValidator(),
        ],
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
        required=True,
        validators=[
            PasswordValidator(),
        ],
    )
    username = serializers.CharField(required=True, min_length=4, max_length=50)


class OutAvatarSerializer(serializers.Serializer[Optional[Profile]]):
    """
    Класс-сериализатор для чтения аватарки пользователя.
    """

    src = serializers.SerializerMethodField()
    alt = serializers.CharField(default="No Image")

    @staticmethod
    def get_src(avatar: Optional[ImageFieldFile]) -> Optional[str]:
        """
        Функция проверит avatar. Если существует, то вернёт его url, иначе None.

        :param avatar: Optional[ImageFieldFile].
        :return: Если существует avatar, то вернёт его url, иначе None.
        """
        if avatar:
            return avatar.url
        return None


class ProfileSerializer(serializers.ModelSerializer[Profile]):
    """
    Класс-сериализатор для профиля пользователя.
    """

    fullName = serializers.CharField(min_length=2, max_length=150, required=True)
    email = serializers.CharField(required=True, validators=[EmailValidator()])
    phone = serializers.CharField(required=True, validators=[PhoneValidator()])
    avatar = OutAvatarSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]


class InAvatarSerializer(serializers.ModelSerializer[Profile]):
    """
    Класс-сериализатор для записи аватарки пользователя.
    """

    avatar = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Profile
        fields = ["avatar"]

    def update(self, instance: Profile, validated_data: Dict[str, Any]) -> Any:
        """Функция удалит старый файл."""

        old_avatar = instance.avatar
        if old_avatar:
            delete_file(old_avatar.path)
        return super().update(instance=instance, validated_data=validated_data)


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
