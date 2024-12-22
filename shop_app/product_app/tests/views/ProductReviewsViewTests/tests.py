
from rest_framework.test import APITestCase

from product_app.models import Tag, Product, SubCategory, Category
from product_app.serializers.review import ReviewSerializer
from product_app.tests.utils import get_category, get_sub_category


class ProductReviewsViewTests(APITestCase):
    """
    Тест ProductReviewsView
    """
    url_view_name = "product_app:product-review"
    product_serializer = ReviewSerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.category = get_category()
        cls.sub_category = get_sub_category(cls.category)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        Tag.objects.all().delete()
        Product.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()
        super().tearDownClass()