from product_app.models import Category
from product_app.serializers.categories import CategorySerializers
from rest_framework.generics import ListAPIView


class CategoryListView(ListAPIView[Category]):
    """
    Класс ListAPIView для модели Category.
    """

    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategorySerializers
