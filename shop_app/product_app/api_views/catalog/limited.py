from django.db.models import Q
from drf_spectacular.utils import extend_schema
from product_app.models import Product
from product_app.serializers.product import OutCatalogProductSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CatalogLimitedAPIView(APIView):
    """
    Класс APIView для продуктов, которые заканчиваются.
    """

    queryset = Product.objects.select_related("category").prefetch_related(
        "tags", "images", "reviews", "sales"
    )
    product_serializer = OutCatalogProductSerializer
    limit = 4
    count = 10

    @extend_schema(
        request=None,
        responses=OutCatalogProductSerializer(many=True),
        description=f"Получение продуктов, которые заканчиваются. (топ {limit})",
        tags=("Catalog",),
    )
    def get(self, request: Request) -> Response:
        """
        Получение продуктов, которые заканчиваются. (топ 4)

        :param request: Request.
        :return: Response.
        """
        products = self.queryset.filter(Q(count__lte=self.count) & Q(archived=False))[
            : self.limit
        ]
        return Response(self.product_serializer(products, many=True).data)
