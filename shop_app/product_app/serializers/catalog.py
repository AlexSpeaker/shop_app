from decimal import Decimal
from typing import Any, Dict

from django.core.paginator import Page
from product_app.models import Product, Sale
from product_app.serializers.product import (
    OutCatalogProductSerializer,
    OutCatalogSaleProductSerializer,
)
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

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Дополнительная валидация для параметров фильтра.

        :param data: Dict[str, Any].
        :return: Dict[str, Any].
        """
        if data["minPrice"] > data["maxPrice"]:
            raise serializers.ValidationError(
                "Минимальная цена не может быть больше максимальной цены."
            )
        return data


class InCatalogSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Serializer каталога входящих данных.
    """

    filter = InFilterSerializer(allow_null=False, required=True)

    currentPage = serializers.IntegerField(allow_null=False, required=True, min_value=1)
    category = serializers.IntegerField(allow_null=False, min_value=1, required=False)
    sort = serializers.ChoiceField(
        choices=[
            ("rating", "rating"),
            ("price", "price"),
            ("reviews", "reviews"),
            ("date", "date"),
        ],
        required=True,
    )
    sortType = serializers.ChoiceField(
        choices=[("inc", "inc"), ("dec", "dec")], required=True
    )
    limit = serializers.IntegerField(allow_null=False, required=True, min_value=1)
    tags = serializers.ListField(
        required=False, allow_empty=False, child=serializers.IntegerField(min_value=1)
    )


class InCurrentPageSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Serializer для текущей страницы.
    """

    currentPage = serializers.IntegerField(allow_null=False, required=True, min_value=1)


class OutCatalogSalesSerializer(serializers.Serializer[Page[Sale]]):
    """
    Serializer каталога исходящих данных (продукты с действующей акцией).
    """

    items = OutCatalogSaleProductSerializer(
        many=True, read_only=True, source="object_list"
    )
    currentPage = serializers.IntegerField(read_only=True, source="number")
    lastPage = serializers.IntegerField(read_only=True, source="paginator.num_pages")
