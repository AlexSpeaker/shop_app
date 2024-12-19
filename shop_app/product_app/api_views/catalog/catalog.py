from django.db.models import Case, DecimalField, Q, When
from product_app.models import Product
from product_app.serializers.catalog import InCatalogSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import parser_query_params


class CatalogAPIView(APIView):
    """
    Класс APIView для каталога.
    """

    query_serializer = InCatalogSerializer
    queryset = Product.objects.select_related("category").prefetch_related(
        "tags", "images", "reviews", "sales"
    )

    def get(self, request: Request) -> Response:
        """
        Получение списка продуктов с учётом переданных параметров.

        :param request: Request.
        :return: Response.
        """
        query_data = request.GET.dict()
        data = parser_query_params(query_data)
        q_serializer = self.query_serializer(data=data)
        if not q_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        filter_data = q_serializer.validated_data["filter"]
        filter_name = Q(title__icontains=filter_data["name"])
        filter_free_delivery = Q(free_delivery=filter_data["freeDelivery"])
        filter_available = Q(count__gt=0) if filter_data["available"] else Q(count=0)

        pre_products = self.queryset.filter(
            filter_name & filter_free_delivery & filter_available
        )

        return Response({})
