from django.db import transaction
from django.db.models import Q
from order_app.api_views.utils import get_basket
from order_app.models import Basket
from order_app.serializers.basket import InBasketSerializer, OutBasketSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


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
        with transaction.atomic():
            serializer_in = self.basket_in_serializer(data=request.data)
            if not serializer_in.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            product, count = serializer_in.validated_data
            basket = get_basket(request, product, count)
            basket.save()
            product.count -= count
            product.save()

        all_baskets = self.queryset.filter(
            Q(user=basket.user) & Q(session_id=basket.session_id)
        )

        return Response(self.basket_out_serializer(all_baskets, many=True).data)
