from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Q
from order_app.models import Basket
from order_app.models.order import Order
from order_app.serializers.order import OutOrderSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import get_or_create_anonymous_user_id


class OrderAPIView(APIView):
    """
    Order APIView
    """

    queryset = Order.objects.prefetch_related("baskets")
    order_out_serializer = OutOrderSerializer

    @staticmethod
    def post(request: Request) -> Response:
        """
        Создание заказа.

        :param request: Request.
        :return: Response.
        """

        user: Optional[AbstractBaseUser] = (
            request.user if request.user.is_authenticated else None
        )
        anonymous_user_id = get_or_create_anonymous_user_id(request)
        all_baskets = Basket.objects.filter(
            Q(user=user) & Q(session_id=anonymous_user_id) & Q(order=None)
        )
        order = Order(user=user, session_id=anonymous_user_id)
        if user:
            order.full_name = user.profile.full_name
            order.email = user.profile.email
            order.phone = user.profile.phone
        order.save()
        order.baskets.add(*all_baskets)
        return Response({"orderId": order.pk})

    def get(self, request: Request) -> Response:
        """
        Получение списка заказов.

        :param request: Request.
        :return: Response.
        """
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        orders = self.queryset.filter(user=request.user)
        serializer = self.order_out_serializer(orders, many=True)
        return Response(data=serializer.data)
