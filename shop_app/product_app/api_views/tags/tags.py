from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter

from product_app.models import Tag
from product_app.serializers.category import InCategoryIDSerializer
from product_app.serializers.tag import OutTagSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class TagAPIView(APIView):
    """
    Класс APIView для тегов.
    """

    queryset = Tag.objects.prefetch_related("products")
    tag_serializer = OutTagSerializer
    id_category_serializer = InCategoryIDSerializer

    @extend_schema(
        request=None,
        responses=OutTagSerializer,
        description="Получение первых популярных тегов категории.",
        tags=("Tags",),
        parameters=[
            OpenApiParameter(
                "category",
                str,
                description="ID подкатегории.",
                required=True,
            ),
        ],
    )
    def get(self, request: Request) -> Response:
        """
        Получение первых популярных тегов категории.

        :param request: Request.
        :return: Response.
        """

        category_id = request.query_params.get("category", None)
        id_serializer = self.id_category_serializer(data={"category_id": category_id})
        if not id_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        tags = (
            self.queryset.filter(products__category_id=category_id)
            .annotate(products_count=Count("products"))
            .order_by("-products_count")[:10]
        )
        serializer = self.tag_serializer(tags, many=True)
        return Response(serializer.data)
