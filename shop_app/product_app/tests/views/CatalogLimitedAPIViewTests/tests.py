from random import choice, choices

from django.urls import reverse
from product_app.api_views.catalog.limited import CatalogLimitedAPIView
from product_app.models import Category, Product, SubCategory
from product_app.tests.utils import get_category, get_simple_product, get_sub_category
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class CatalogLimitedAPIViewTests(APITestCase):
    """
    Тест CatalogLimitedAPIView.
    """

    url = reverse("product_app:product-limited")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.product_limit_count = CatalogLimitedAPIView.count
        cls.limit_in_page = CatalogLimitedAPIView.limit
        cls.category = get_category()
        cls.sub_categories = [
            get_sub_category(cls.category),
            get_sub_category(cls.category),
        ]
        cls.products = [
            get_simple_product(choice(cls.sub_categories)) for _ in range(10)
        ]
        cls.products_limit = choices(cls.products, k=5)
        for product in cls.products_limit:
            product.count = cls.product_limit_count - 1
        Product.objects.bulk_update(cls.products_limit, ["count"])

    def test_get_limit_products(self) -> None:
        """
        Проверяем, что нам возвращаются продукты, которые заканчиваются.

        :return: None.
        """
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(len(response.data) <= self.limit_in_page)
        set_ids_limit_products = {product.pk for product in self.products_limit}
        set_ids_in_response = {product["id"] for product in response.data}
        self.assertTrue(set_ids_in_response.issubset(set_ids_limit_products))

    def test_archived_products(self) -> None:
        """
        Проверим, чтобы в выдаче не было архивированных продуктов.
        :return:
        """
        for product in self.products:
            product.archived = True
        Product.objects.bulk_update(self.products_limit, ["archived"])
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 0)

    def tearDown(self) -> None:
        """
        Возвращаем продуктам archived = False

        :return: None.
        """
        for product in self.products_limit:
            product.archived = False
        Product.objects.bulk_update(self.products_limit, ["archived"])

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        Product.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()
        super().tearDownClass()
