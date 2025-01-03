from django.db import transaction
from django.db.models import Q
from drf_spectacular.utils import OpenApiResponse, extend_schema
from order_app.models import Basket
from order_app.serializers.basket import (
    InBasketSerializer,
    InDeleteBasketSerializer,
    OutBasketSerializer,
)
from product_app.models import Product
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import CustomAutoSchema, get_or_create_anonymous_user_id


class BasketAPIView(APIView):
    """
    Basket APIView
    """

    schema = CustomAutoSchema()
    basket_in_serializer = InBasketSerializer
    basket_in_delete_serializer = InDeleteBasketSerializer
    basket_out_serializer = OutBasketSerializer
    queryset = Basket.objects.select_related(
        "product", "product__category", "user"
    ).prefetch_related(
        "product__tags", "product__images", "product__reviews", "product__sales"
    )

    @extend_schema(
        request=InBasketSerializer,
        responses={
            200: OutBasketSerializer(many=True),
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Создание корзины.",
        tags=("Basket",),
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
                user=user, product=product, session_id=anonymous_user_id, order=None
            )
            basket.count += count
            basket.save()
            product.count -= count
            product.save()

        all_baskets = self.queryset.filter(
            Q(user=user) & Q(session_id=anonymous_user_id) & Q(order=None)
        )

        return Response(self.basket_out_serializer(all_baskets, many=True).data)

    @extend_schema(
        request=None,
        responses=OutBasketSerializer(many=True),
        description="Получение списка корзин.",
        tags=("Basket",),
    )
    def get(self, request: Request) -> Response:
        """
        Получение списка корзин.

        :param request: Request.
        :return: Response.
        """
        user = request.user if request.user.is_authenticated else None
        anonymous_user_id = get_or_create_anonymous_user_id(request)
        all_baskets = self.queryset.filter(
            Q(user=user) & Q(session_id=anonymous_user_id) & Q(order=None)
        )

        return Response(self.basket_out_serializer(all_baskets, many=True).data)

    @extend_schema(
        request=InDeleteBasketSerializer,
        responses={
            200: OutBasketSerializer(many=True),
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Удаление единицы продукта из корзины. При количестве товара равное 0, удаляется сама корзина.",
        tags=("Basket",),
    )
    def delete(self, request: Request) -> Response:
        """
        Удаление единицы продукта из корзины.
        При количестве товара равное 0, удаляется сама корзина.

        :param request: Request.
        :return: Response.
        """
        serializer_in = self.basket_in_delete_serializer(data=request.data)
        user = request.user if request.user.is_authenticated else None
        anonymous_user_id = get_or_create_anonymous_user_id(request)
        if not serializer_in.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            data = serializer_in.validated_data
            product: Product = (
                Product.objects.select_for_update().filter(pk=data["id"]).first()
            )
            if not product:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            basket: Basket = (
                self.queryset.select_for_update()
                .filter(
                    Q(product=product)
                    & Q(user=user)
                    & Q(session_id=anonymous_user_id)
                    & Q(order=None)
                )
                .first()
            )
            if not basket:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if data["count"] >= basket.count:
                product.count += basket.count
                product.save()
                basket.delete()
            else:
                product.count += data["count"]
                basket.count -= data["count"]
                basket.save()
                product.save()
        all_baskets = self.queryset.filter(
            Q(user=user) & Q(session_id=anonymous_user_id) & Q(order=None)
        )

        return Response(self.basket_out_serializer(all_baskets, many=True).data)
