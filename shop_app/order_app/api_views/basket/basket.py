from django.db import transaction
from django.db.models import Q
from order_app.models import Basket
from order_app.serializers.basket import InBasketSerializer, OutBasketSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import get_or_create_anonymous_user_id


class BasketAPIView(APIView):
    """
    Basket APIView
    """

    basket_in_serializer = InBasketSerializer
    basket_out_serializer = OutBasketSerializer
    queryset = Basket.objects.select_related(
        "product", "product__category"
    ).prefetch_related(
        "product__tags", "product__images", "product__reviews", "product__sales"
    )

    def post(self, request: Request) -> Response:
        """
        Создание корзины.

        :param request: Request.
        :return: Response.
        """
        user = request.user if request.user.is_authenticated else None
        anonymous_user_id = get_or_create_anonymous_user_id(request)

        with transaction.atomic():
            serializer_in = self.basket_in_serializer(data=request.data)
            if not serializer_in.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            product, count = serializer_in.validated_data
            basket, _ = Basket.objects.get_or_create(
                user=user, product=product, session_id=anonymous_user_id
            )
            basket.count += count
            basket.save()
            product.count -= count
            product.save()

        all_baskets = self.queryset.filter(
            Q(user=user) & Q(session_id=anonymous_user_id)
        )

        return Response(self.basket_out_serializer(all_baskets, many=True).data)

    def get(self, request: Request) -> Response:
        """
        Получение списка корзин.

        :param request: Request.
        :return: Response.
        """
        user = request.user if request.user.is_authenticated else None
        anonymous_user_id = get_or_create_anonymous_user_id(request)
        all_baskets = self.queryset.filter(
            Q(user=user) & Q(session_id=anonymous_user_id)
        )

        return Response(self.basket_out_serializer(all_baskets, many=True).data)
