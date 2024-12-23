from random import choice

from django.urls import reverse
from product_app.api_views.catalog.banners import CatalogBannersAPIView
from product_app.models import Category, Product, SubCategory
from product_app.tests.utils import get_category, get_simple_product, get_sub_category
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class CatalogBannersAPIViewTests(APITestCase):
    """
    Тест CatalogBannersAPIView.
    """

    url = reverse("product_app:banners")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.category = get_category()
        cls.sub_categories = [
            get_sub_category(cls.category),
            get_sub_category(cls.category),
        ]
        cls.products = [
            get_simple_product(choice(cls.sub_categories)) for _ in range(10)
        ]

    def test_get_banners(self) -> None:
        """
        Проверяем получение случайных продуктов.
        :return: None.
        """
        limit = CatalogBannersAPIView.limit
        response_1: Response = self.client.get(self.url)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        response_2: Response = self.client.get(self.url)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        # Когда дело касается случайностей, то есть вероятность,
        # что звёзды на небе сойдутся так, что этот тест провалится, поэтому перепроверяем.
        self.assertFalse(response_1.data == response_2.data)
        self.assertEqual(len(response_1.data), len(response_2.data))
        self.assertTrue(len(response_1.data) <= limit)
        set_keys = {
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        }
        self.assertEqual(set(response_1.data[0].keys()), set_keys)

    def test_archived_products(self) -> None:
        """
        Проверим, чтобы в выдаче не было архивированных продуктов.
        :return:
        """

        for product in self.products[:-1]:
            product.archived = True
        Product.objects.bulk_update(self.products, ["archived"])
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def tearDown(self) -> None:
        """
        Возвращаем продуктам archived = False

        :return: None.
        """
        for product in self.products:
            product.archived = False
        Product.objects.bulk_update(self.products, ["archived"])

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
