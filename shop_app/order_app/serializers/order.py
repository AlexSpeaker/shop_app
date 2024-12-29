from decimal import Decimal

from order_app.models.order import Order
from order_app.serializers.basket import OutBasketSerializer
from rest_framework import serializers


class OutOrderSerializer(serializers.ModelSerializer[Order]):
    """
    Serializer Order исходящих данных.
    """

    id = serializers.IntegerField(read_only=True, source="pk")
    createdAt = serializers.DateTimeField(
        read_only=True, source="created_at", format="%Y-%m-%d %H:%M"
    )
    fullName = serializers.CharField(read_only=True, source="full_name")
    deliveryType = serializers.CharField(read_only=True, source="delivery_type")
    paymentType = serializers.CharField(read_only=True, source="payment_type")
    totalCost = serializers.SerializerMethodField(
        method_name="get_total_cost", read_only=True
    )
    products = OutBasketSerializer(many=True, read_only=True, source="baskets")

    class Meta:
        model = Order
        fields = (
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        )

    @staticmethod
    def get_total_cost(obj: Order) -> Decimal:
        """
        Функция возвращает полную стоимость заказа.

        :param obj: Order.
        :return: Decimal.
        """
        return Decimal(
            sum(
                [
                    (
                        (
                            basket.fixed_price
                            if basket.fixed_price
                            else basket.product.get_actual_price()
                        )
                        * basket.count
                    )
                    for basket in obj.baskets.all()
                ]
            )
        )


class InOrderSerializer(serializers.ModelSerializer[Order]):
    """
    Serializer Order входящих данных.
    """

    fullName = serializers.CharField(write_only=True, source="full_name", required=True)
    deliveryType = serializers.CharField(
        write_only=True, source="delivery_type", allow_null=True
    )
    paymentType = serializers.CharField(
        write_only=True, source="payment_type", allow_null=True
    )

    class Meta:
        fields = (
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "city",
            "address",
        )
        model = Order
        extra_kwargs = {
            "email": {"required": True},
            "phone": {"required": True},
            "city": {"required": True},
            "address": {"required": True},
        }


class OutOrderIDSerializer(serializers.Serializer[Order]):
    """
    Serializer Order ID исходящих данных.
    """

    orderId = serializers.IntegerField(read_only=True, source="pk")

    class Meta:
        fields = ("orderId",)
        model = Order
