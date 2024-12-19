from decimal import Decimal
from typing import Any, Dict

from django.core.paginator import Page
from product_app.models import Product
from product_app.serializers.product import OutCatalogProductSerializer
from rest_framework import serializers


class OutCatalogSerializer(serializers.Serializer[Page[Product]]):
    """
    Serializer каталога исходящих данных.
    """

    items = OutCatalogProductSerializer(many=True, read_only=True, source="object_list")
    currentPage = serializers.IntegerField(read_only=True, source="number")
    lastPage = serializers.IntegerField(read_only=True, source="paginator.num_pages")


class InFilterSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Serializer для фильтра каталога входящих данных.
    """

    name = serializers.CharField(
        max_length=500,
        allow_null=False,
        required=True,
        allow_blank=True,
    )
    minPrice = serializers.DecimalField(
        required=True,
        max_digits=10,
        decimal_places=2,
        allow_null=False,
        min_value=Decimal("0"),
    )
    maxPrice = serializers.DecimalField(
        required=True,
        max_digits=10,
        decimal_places=2,
        allow_null=False,
        min_value=Decimal("0"),
    )
    freeDelivery = serializers.BooleanField(allow_null=False, required=True)
    available = serializers.BooleanField(allow_null=False, required=True)


class InCatalogSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Serializer каталога входящих данных.
    """

    filter = InFilterSerializer(allow_null=False, required=True)

    currentPage = serializers.IntegerField(allow_null=False, required=True, min_value=1)
    category = serializers.IntegerField(allow_null=False, required=True, min_value=1)
    sort = serializers.ChoiceField(
        choices=[
            ("rating", "rating"),
            ("price", "price"),
            ("reviews", "reviews"),
            ("date", "date"),
        ],
        required=False,
    )
    sortType = serializers.ChoiceField(
        choices=[("inc", "inc"), ("dec", "dec")], required=False
    )
    limit = serializers.IntegerField(allow_null=False, required=True, min_value=1)