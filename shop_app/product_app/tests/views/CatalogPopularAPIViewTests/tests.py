from random import choice

from django.urls import reverse
from product_app.api_views.catalog.popular import CatalogPopularAPIView
from product_app.models import Category, Product, SubCategory
from product_app.tests.utils import (
    get_category,
    get_review,
    get_simple_product,
    get_sub_category,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class CatalogPopularAPIViewTests(APITestCase):
    """
    Тест CatalogPopularAPIView.
    """

    url = reverse("product_app:product-popular")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.category = get_category()
        cls.limit_in_page = CatalogPopularAPIView.limit
        cls.sub_categories = [
            get_sub_category(cls.category),
            get_sub_category(cls.category),
        ]
        cls.products = [
            get_simple_product(choice(cls.sub_categories)) for _ in range(10)
        ]
        for product in cls.products[:-1]:
            for _ in range(20):
                get_review(product)

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        for product in self.products:
            product.archived = False
        Product.objects.bulk_update(self.products, ["archived"])

    def test_get_popular_products(self) -> None:
        """
        Проверяем, что нам возвращаются продукты, которые имеют максимальную оценку.

        :return: None.
        """
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        products_top_rating = sorted(
            [product.get_rating() for product in self.products], reverse=True
        )
        response_top_rating = [product["rating"] for product in response.data]
        self.assertEqual(products_top_rating[: self.limit_in_page], response_top_rating)

    def test_archived_products(self) -> None:
        """
        Проверим, чтобы в выдаче не было архивированных продуктов.

        :return:
        """
        for product in self.products:
            product.archived = True
        Product.objects.bulk_update(self.products, ["archived"])
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

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
