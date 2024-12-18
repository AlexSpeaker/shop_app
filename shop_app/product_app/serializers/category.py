from typing import Any, Optional

from django.db.models.fields.files import ImageFieldFile
from product_app.models import Category, SubCategory
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


class OutSubCategorySerializer(serializers.ModelSerializer[SubCategory]):
    """
    Serializer для SubCategory.
    """

    title = serializers.CharField(read_only=True, source="name")
    id = serializers.IntegerField(read_only=True, source="pk")
    image = OutImageSerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = "id", "title", "image"


class OutCategorySerializer(serializers.ModelSerializer[Category]):
    """
    Serializer для Category.
    """

    title = serializers.CharField(read_only=True, source="name")
    id = serializers.IntegerField(read_only=True, source="pk")
    image = OutImageSerializer(read_only=True)
    subcategories = OutSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "id", "title", "image", "subcategories"
