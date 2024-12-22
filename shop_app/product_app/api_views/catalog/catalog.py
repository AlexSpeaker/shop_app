from django.core.paginator import Paginator
from django.db.models import Avg, Case, Count, DecimalField, F, Q, When
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from product_app.api_views.catalog.utils import get_catalog_filters, get_catalog_sort
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

    @extend_schema(
        request=None,
        responses={
            200: OutCatalogSerializer,
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Получение списка продуктов с учётом заданных параметров.",
        tags=("Catalog",),
        parameters=[
            OpenApiParameter(
                "filter[name]",
                str,
                description="Фильтр по имени продукта.",
                required=True,
            ),
            OpenApiParameter(
                "filter[minPrice]",
                float,
                description="Минимальная цена продукта.",
                required=True,
            ),
            OpenApiParameter(
                "filter[maxPrice]",
                float,
                description="Максимальная цена продукта.",
                required=True,
            ),
            OpenApiParameter(
                "filter[freeDelivery]",
                bool,
                description="Фильтр по бесплатной доставке.",
                required=True,
            ),
            OpenApiParameter(
                "filter[available]",
                bool,
                description="Фильтр по доступности продукта.",
                required=True,
            ),
            OpenApiParameter(
                "currentPage", int, description="Номер текущей страницы.", required=True
            ),
            OpenApiParameter(
                "category", int, description="ID категории продукта.", required=False
            ),
            OpenApiParameter(
                "sort",
                str,
                description="Параметр сортировки (например, 'price').",
                required=True,
            ),
            OpenApiParameter(
                "sortType",
                str,
                description="Тип сортировки (например, 'inc' или 'dec').",
                required=True,
            ),
            OpenApiParameter(
                "limit",
                int,
                description="Количество продуктов на странице.",
                required=True,
            ),
            OpenApiParameter(
                name="tags[]",
                type={"type": "array", "items": {"type": "integer"}},
                description="Список id тегов для фильтрации.",
                required=False,
            ),
        ],
    )
    def get(self, request: Request) -> Response:
        """
        Получение списка продуктов с учётом переданных параметров.

        :param request: Request.
        :return: Response.
        """
        query_data = request.GET
        data = parser_query_params(query_data)
        q_serializer = self.query_serializer(data=data)
        if not q_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Получаем фильтры.
        filter_params = get_catalog_filters(q_serializer.validated_data)

        # Получаем сортировку.
        sort = get_catalog_sort(q_serializer.validated_data)

        # Если у продукта есть действующая акция,
        # то final_price будет от акции, иначе от продукта,
        # и всё это дело пропускаем через фильтр max_price и min_price плюс созданные фильтры выше.
        products = (
            self.queryset.annotate(
                final_price=Case(
                    # Если акция активна, используем цену со скидкой
                    # (действующая акция может быть только одна).
                    When(
                        Q(sales__date_from__lte=timezone.now().date())
                        & Q(sales__date_to__gte=timezone.now().date()),
                        then=F("sales__sale_price"),
                    ),
                    # Иначе используем стандартную цену.
                    default=F("price"),
                    output_field=DecimalField(),
                ),
                # Добавим недостающие поля для продуктов (для сортировки).
                reviews_count=Count("reviews"),
                rating=Case(
                    # Если отзывы есть, то считаем среднее значение рейтинга.
                    When(reviews_count__gt=0, then=Avg("reviews__rate")),
                    # Иначе 0.
                    default=0,
                    output_field=DecimalField(),
                ),
            )
            .filter(
                # Фильтруем по заданным параметрам.
                Q(final_price__gte=q_serializer.validated_data["filter"]["minPrice"])
                & Q(final_price__lte=q_serializer.validated_data["filter"]["maxPrice"])
                & filter_params
            )
            .order_by(sort)
        )

        paginator = Paginator(products, q_serializer.validated_data["limit"])
        page_odj = paginator.get_page(q_serializer.validated_data["currentPage"])

        return Response(data=self.catalog_serializer(page_odj).data)
