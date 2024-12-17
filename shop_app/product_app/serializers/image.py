from typing import Any, Optional

from django.db.models.fields.files import ImageFieldFile
from rest_framework import serializers


class OutImageSerializer(serializers.Serializer[Any]):
    """
    Serializer класс для обычной картинки.
    """

    src = serializers.SerializerMethodField()
    alt = serializers.CharField(default="No Image")

    @staticmethod
    def get_src(image: Optional[ImageFieldFile]) -> Optional[str]:
        """
        Функция проверит image. Если существует, то вернёт его url, иначе None.

        :param image: Optional[ImageFieldFile].
        :return: Если существует image, то вернёт его url, иначе None.
        """
        if image:
            return image.url
        return None
