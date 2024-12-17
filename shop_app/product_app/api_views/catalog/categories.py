from typing import Any

from drf_spectacular.utils import extend_schema

from product_app.models import Category
from product_app.serializers.categories import CategorySerializers
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class CategoryListView(ListAPIView[Category]):
    """
    Класс ListAPIView для модели Category.
    """

    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategorySerializers

    @extend_schema(
        request=None,
        responses=CategorySerializers,
        description="Получение списка категорий.",
        tags=("Catalog",),
    )
    def get(self, *args: Any, **kwargs: Any) -> Response:
        return super().get(*args, **kwargs)
