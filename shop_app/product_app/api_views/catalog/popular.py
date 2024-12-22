from django.db.models import Avg, Case, Count, DecimalField, When
from drf_spectacular.utils import extend_schema

from product_app.models import Product
from product_app.serializers.product import OutCatalogProductSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CatalogPopularAPIView(APIView):
    """
    Класс APIView для самых (топ 4) популярных продуктов во всём каталоге.
    """

    queryset = Product.objects.select_related("category").prefetch_related(
        "tags", "images", "reviews", "sales"
    )
    product_serializer = OutCatalogProductSerializer
    limit = 4

    @extend_schema(
        request=None,
        responses=OutCatalogProductSerializer(many=True),
        description=f"Получение топ {limit} популярных продуктов во всём каталоге.",
        tags=("Catalog",),
    )
    def get(self, request: Request) -> Response:
        """
        Получение топ 4 популярных продуктов во всём каталоге.

        :param request: Request.
        :return: Response.
        """

        products = self.queryset.annotate(
            reviews_count=Count("reviews"),
            rating=Case(
                # Если отзывы есть, то считаем среднее значение рейтинга.
                When(reviews_count__gt=0, then=Avg("reviews__rate")),
                # Иначе 0.
                default=0,
                output_field=DecimalField(),
            ),
        ).order_by("-rating")[: self.limit]
        return Response(self.product_serializer(products, many=True).data)
