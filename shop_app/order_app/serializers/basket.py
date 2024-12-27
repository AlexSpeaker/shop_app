from decimal import Decimal
from typing import Any, Dict

from order_app.models import Basket
from product_app.models import Product
from product_app.serializers.product import OutProductImageSerializer
from product_app.serializers.tag import OutTagSerializer
from rest_framework import serializers


class InBasketSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Serializer Basket входящих данных.
    """

    id = serializers.IntegerField(min_value=1, required=True, write_only=True)
    count = serializers.IntegerField(min_value=1, required=True, write_only=True)

    def validate(self, data: Dict[str, Any]) -> tuple[Product, int]:
        """
        Дополнительная валидация. Проверим, есть ли товар с запрашиваемыми данными.
        Возвращает кортеж: связанный продукт, необходимое количество.

        :param data: Dict[str, Any].
        :return: Связанный продукт, необходимое количество.
        """
        data = super().validate(data)
        product = Product.objects.select_for_update().filter(pk=data["id"]).first()
        if not product:
            raise serializers.ValidationError(
                f"Продукта с ID={data['id']} не существует."
            )
        elif product.count < data["count"]:
            raise serializers.ValidationError(
                f"Продуктов всего {product.count}, а запрашивается {data['count']}."
            )
        return product, data["count"]


class OutBasketSerializer(serializers.ModelSerializer[Basket]):
    """
    Serializer Basket исходящих данных.
    """

    id = serializers.IntegerField(read_only=True, source="product.pk")
    category = serializers.IntegerField(read_only=True, source="product.category.pk")
    price = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateTimeField(read_only=True, source="product.created_at")
    title = serializers.CharField(read_only=True, source="product.title")
    description = serializers.CharField(read_only=True, source="product.description")
    freeDelivery = serializers.BooleanField(
        read_only=True, source="product.free_delivery"
    )
    images = OutProductImageSerializer(
        many=True, read_only=True, source="product.images"
    )
    tags = OutTagSerializer(many=True, read_only=True, source="product.tags")
    reviews = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Basket
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )

    @staticmethod
    def get_price(obj: Basket) -> Decimal:
        """
        Определит текущую цену на продукт (учитывает действующую акцию).
        Если покупка уже совершена, то вернёт цену по которой была совершена покупка.

        :param obj: Product.
        :return: Цена.
        """
        if obj.fixed_price:
            return obj.fixed_price
        actual_price: Decimal = obj.product.get_actual_price()
        return actual_price

    @staticmethod
    def get_reviews(obj: Basket) -> int:
        """
        Определит количество отзывов.

        :return: Количество отзывов
        """
        reviews_count: int = obj.product.reviews.count()
        return reviews_count

    @staticmethod
    def get_rating(obj: Basket) -> float:
        """
        Функция определит средний рейтинг продукта.

        :param obj: Product.
        :return: Средний рейтинг продукта.
        """
        rating: float = obj.product.get_rating()
        return rating


class InDeleteBasketSerializer(serializers.Serializer[Dict[str, Any]]):
    """
    Serializer Basket входящих данных (удаление корзины).
    """

    id = serializers.IntegerField(min_value=1, required=True, write_only=True)
    count = serializers.IntegerField(min_value=1, required=True, write_only=True)
