from product_app.models import Category, SubCategory
from product_app.serializers.image import OutImageSerializer
from rest_framework import serializers


class SubCategorySerializers(serializers.ModelSerializer[SubCategory]):
    """
    Serializer для SubCategory.
    """

    title = serializers.CharField(read_only=True, source="name")
    id = serializers.IntegerField(read_only=True, source="pk")
    image = OutImageSerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = "id", "title", "image"


class CategorySerializers(serializers.ModelSerializer[Category]):
    """
    Serializer для Category.
    """

    title = serializers.CharField(read_only=True, source="name")
    id = serializers.IntegerField(read_only=True, source="pk")
    image = OutImageSerializer(read_only=True)
    subcategories = SubCategorySerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "id", "title", "image", "subcategories"
