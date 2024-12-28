from typing import Optional

from drf_spectacular.utils import OpenApiResponse, extend_schema
from order_app.models.order import Order
from order_app.serializers.order import (
    InOrderSerializer,
    OutOrderIDSerializer,
    OutOrderSerializer,
)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class OrderIdAPIView(APIView):
    """
    OrderId APIView
    """

    queryset = Order.objects.select_related("user").prefetch_related(
        "baskets",
        "baskets__product",
        "baskets__product__category",
        "baskets__user",
        "baskets__product__tags",
        "baskets__product__images",
        "baskets__product__reviews",
        "baskets__product__sales",
    )
    order_out_serializer = OutOrderSerializer
    order_out_id_serializer = OutOrderIDSerializer
    order_in_serializer = InOrderSerializer

    @extend_schema(
        request=None,
        responses={
            200: order_out_serializer,
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Получение информации о заказе.",
        tags=("Order",),
    )
    def get(self, request: Request, order_id: int) -> Response:
        """
        Получение информации о заказе.

        :param request: Request.
        :param order_id: ID заказа.
        :return: Response.
        """
        order = self.queryset.filter(pk=order_id).first()
        if not order:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(OutOrderSerializer(order).data)

    @extend_schema(
        request=order_in_serializer,
        responses={
            200: order_out_id_serializer,
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Обновление данных заказа.",
        tags=("Order",),
    )
    def post(self, request: Request, order_id: int) -> Response:
        """
        Обновление данных заказа.

        :param request: Request.
        :param order_id: ID заказа.
        :return: Response.
        """
        order: Optional[Order] = self.queryset.filter(pk=order_id).first()
        if not order:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.order_in_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.update(order, serializer.validated_data)
        return Response(self.order_out_id_serializer(order).data)
