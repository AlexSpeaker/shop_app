from product_app.models import Tag
from rest_framework import serializers


class OutTagSerializer(serializers.ModelSerializer[Tag]):
    """
    Serializer класс для тегов.
    """

    id = serializers.IntegerField(read_only=True, source="pk")
    name = serializers.CharField(read_only=True, source="name")

    class Meta:
        model = Tag
        fields = ("id", "name")
