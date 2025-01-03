from drf_spectacular.utils import extend_schema
from product_app.models import Product
from product_app.serializers.product import OutCatalogProductSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CatalogBannersAPIView(APIView):
    """
    Класс APIView для случайных продуктов.
    """

    queryset = Product.objects.select_related("category").prefetch_related(
        "tags", "images", "reviews", "sales"
    )
    product_serializer = OutCatalogProductSerializer
    limit = 4

    @extend_schema(
        request=None,
        responses=OutCatalogProductSerializer(many=True),
        description=f"Получение {limit} случайных продуктов.",
        tags=("Catalog",),
    )
    def get(self, request: Request) -> Response:
        """
        Получение 4 случайных продуктов.

        :param request: Request.
        :return: Response.
        """
        products = self.queryset.filter(archived=False).order_by("?")[: self.limit]
        return Response(self.product_serializer(products, many=True).data)
