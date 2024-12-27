from typing import Optional

from order_app.models.order import Order
from order_app.serializers.order import InOrderSerializer, OutOrderSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class OrderIdAPIView(APIView):
    """
    OrderId APIView
    """

    queryset = Order.objects.prefetch_related("baskets")
    order_out_serializer = OutOrderSerializer
    order_in_serializer = InOrderSerializer

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
        print(serializer.validated_data)
        serializer.update(order, serializer.validated_data)
        return Response({"orderId": order.pk})
