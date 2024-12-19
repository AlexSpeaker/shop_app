from django.core.paginator import Paginator
from django.db.models import Avg, Case, DecimalField, F, Q, When, Count
from django.utils import timezone
from product_app.models import Product
from product_app.serializers.catalog import InCatalogSerializer, OutCatalogSerializer
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
    catalog_serializer = OutCatalogSerializer

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
        category = Q(category__id=q_serializer.validated_data["category"])

        pre_products_with_filter = self.queryset.filter(
            filter_name & filter_free_delivery & filter_available & category
        )
        products_with_filter = pre_products_with_filter.annotate(
            final_price=Case(
                # Если акция активна, используем цену со скидкой
                When(
                    Q(sales__date_from__lte=timezone.now().date())
                    & Q(sales__date_to__gte=timezone.now().date()),
                    then=F("sales__sale_price"),
                ),
                # Иначе используем стандартную цену
                default=F("price"),
                output_field=DecimalField(),
            )
        ).filter(
            final_price__gte=filter_data["minPrice"],
            final_price__lte=filter_data["maxPrice"],
        )

        if q_serializer.validated_data["sort"] == "price":
            pre_sort = "final_price"
        elif q_serializer.validated_data["sort"] == "reviews":
            pre_sort = "reviews_count"
        elif q_serializer.validated_data["sort"] == "date":
            pre_sort = "created_at"
        else:
            pre_sort = q_serializer.validated_data["sort"]

        sort = (
            f"-{pre_sort}"
            if q_serializer.validated_data["sortType"] == "dec"
            else pre_sort
        )
        products = products_with_filter.annotate(
            rating=Avg("reviews__rate"), reviews_count=Count("reviews")
        ).order_by(sort)

        paginator = Paginator(products, q_serializer.validated_data["limit"])
        page_odj = paginator.get_page(q_serializer.validated_data["currentPage"])

        return Response(data=self.catalog_serializer(page_odj).data)
