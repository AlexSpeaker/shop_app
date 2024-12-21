from drf_spectacular.utils import OpenApiResponse, extend_schema
from product_app.models import Product
from product_app.serializers.product import OutProductSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import get_or_none


class ProductView(APIView):
    """
    Класс APIView для продуктов.
    """

    queryset = Product.objects.select_related("category").prefetch_related(
        "tags", "images", "reviews", "sales"
    )
    product_serializer = OutProductSerializer

    @extend_schema(
        request=None,
        responses={
            200: OutProductSerializer,
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Получение подробной информации о продукте.",
        tags=("Product",),
    )
    def get(self, request: Request, product_id: int) -> Response:
        """
        Получение подробной информации о продукте.

        :param request: Request.
        :param product_id: ID продукта.
        :return: Response.
        """
        product = get_or_none(self.queryset, id=product_id)
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(self.product_serializer(product).data)
