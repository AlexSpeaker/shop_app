from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from product_app.models import Sale
from product_app.serializers.catalog import (
    InCurrentPageSerializer,
    OutCatalogSalesSerializer,
)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CatalogSalesAPIView(APIView):
    """
    Класс APIView для продуктов с действующей акцией в каталоге.
    """

    queryset = Sale.objects.select_related("product").prefetch_related(
        "product__images"
    )
    catalog_serializer = OutCatalogSalesSerializer
    page_serializer = InCurrentPageSerializer
    limit_on_page = 10

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                "currentPage",
                int,
                description="Текущая страница.",
                required=True,
            ),
        ],
        responses={
            200: OutCatalogSalesSerializer,
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Получение списка продуктов с действующей акцией.",
        tags=("Catalog",),
    )
    def get(self, request: Request) -> Response:
        """
        Получение списка продуктов с действующей акцией.

        :param request: Request.
        :return: Response.
        """
        current_page_serializer = InCurrentPageSerializer(data=request.GET)
        if not current_page_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sales = self.queryset.filter(
            Q(date_from__lte=timezone.now().date())
            & Q(date_to__gte=timezone.now().date())
            & Q(product__archived=False)
        ).order_by("date_to")
        paginator = Paginator(sales, self.limit_on_page)
        page_odj = paginator.get_page(
            current_page_serializer.validated_data["currentPage"]
        )
        return Response(self.catalog_serializer(page_odj).data)
