from django.core.paginator import Page
from product_app.models import Product
from product_app.serializers.product import OutCatalogProductSerializer
from rest_framework import serializers


class OutCatalogSerializer(serializers.Serializer[Page[Product]]):
    """
    Serializer каталога.
    """

    items = OutCatalogProductSerializer(many=True, read_only=True, source="object_list")
    currentPage = serializers.IntegerField(read_only=True, source="number")
    lastPage = serializers.IntegerField(read_only=True, source="paginator.num_pages")
