from typing import Optional

from django.db import transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from order_app.models import Basket
from order_app.models.order import Order
from order_app.serializers.payment import InPaymentSerializer


class PaymentAPIView(APIView):
    """
    Payment APIView
    """
    payment_in_serializer = InPaymentSerializer
    queryset = Order.objects.prefetch_related(
        "baskets",
        "baskets__product",
        "baskets__product__category",
        "baskets__user",
        "baskets__product__tags",
        "baskets__product__images",
        "baskets__product__reviews",
        "baskets__product__sales",
    )

    @extend_schema(
        request=payment_in_serializer,
        responses={
            200: OpenApiResponse(description="Успешная операция."),
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="При успешной проверке помечает заказ как завершённым.",
        tags=("Payment",),
    )
    def post(self, request: Request, order_id: int) -> Response:
        """
        При успешной проверке помечает заказ как завершённым.

        :param request: Request.
        :param order_id: ID заказа.
        :return: Response.
        """
        with transaction.atomic():
            data = request.data
            serializer = self.payment_in_serializer(data=data)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            order: Optional[Order] = self.queryset.select_for_update().filter(pk=order_id).first()
            if not order:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            baskets = order.baskets.all()
            for basket in baskets:
                basket.fixed_price = basket.product.get_actual_price()
            Basket.objects.bulk_update(baskets, ["fixed_price"])
            order.paid_for = True
            order.save()

        return Response(status=status.HTTP_200_OK)