from django.core.paginator import Paginator
from django.test import TestCase
from product_app.models import Category, Product, SubCategory, Tag
from product_app.serializers.catalog import OutCatalogSerializer
from product_app.tests.utils import get_product


class OutCatalogSerializerTests(TestCase):
    """
    Класс Тест для сериализатора OutCatalogSerializer.
    """

    catalog_serializer = OutCatalogSerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.products = [get_product() for _ in range(50)]

    def test_get_data(self) -> None:
        """
        Проверяем: все ли поля на месте.

        :return: None.
        """
        limit = 10
        current_page = 2
        total_pages = len(self.products) // limit

        products = Product.objects.all().order_by("-id")
        paginator = Paginator(products, limit)
        page_odj = paginator.get_page(current_page)
        serializer = self.catalog_serializer(page_odj)
        data = serializer.data

        set_keys = {"items", "currentPage", "lastPage"}
        self.assertEqual(set_keys, set(data.keys()))

        self.assertTrue(len(data["items"]) == limit)
        self.assertTrue(data["currentPage"] == current_page)

        self.assertTrue(data["lastPage"] == total_pages)

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
