from typing import Any, Dict, Optional

from auth_app.models.profile import Profile
from auth_app.utils import delete_file
from django.db.models.fields.files import ImageFieldFile
from rest_framework import serializers


class OutAvatarSerializer(serializers.Serializer[Profile]):
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
