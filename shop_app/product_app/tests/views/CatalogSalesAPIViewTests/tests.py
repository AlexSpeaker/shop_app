from datetime import timedelta
from random import choice, choices, randint

from django.urls import reverse
from django.utils import timezone
from product_app.api_views.catalog.sales import CatalogSalesAPIView
from product_app.models import Category, Product, Sale, SubCategory
from product_app.tests.utils import get_category, get_simple_product, get_sub_category
from rest_framework import status
from rest_framework.test import APITestCase


class CatalogSalesAPIViewTests(APITestCase):
    """
    Тест CatalogSalesAPIView
    """

    url = reverse("product_app:sales")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.category = get_category()
        cls.limit_on_page = CatalogSalesAPIView.limit_on_page
        cls.sub_categories = [
            get_sub_category(cls.category),
            get_sub_category(cls.category),
        ]
        cls.products = [
            get_simple_product(choice(cls.sub_categories)) for _ in range(10)
        ]
        cls.sale_products = choices(cls.products, k=5)
        for product in cls.sale_products:
            Sale.objects.create(
                product=product,
                date_from=timezone.now().date()
                - timedelta(days=1)
                + timedelta(days=randint(0, 2)),
                date_to=timezone.now().date() + timedelta(days=10),
                price=product.price,
                sale_price=product.price - 10,
            )

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        for product in self.sale_products:
            product.archived = False
        Product.objects.bulk_update(self.sale_products, ["archived"])

    def test_get_sale_product(self) -> None:
        """
        Проверяем, что нам возвращаются продукты, которые имеют действующую акцию.

        :return: None.
        """
        response = self.client.get(self.url, data={"currentPage": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_ids_set = {product.pk for product in self.sale_products}
        response_product_ids_set = {item["id"] for item in response.data["items"]}
        self.assertTrue(response_product_ids_set.issubset(product_ids_set))

    def test_no_current_page(self) -> None:
        """
        Проверяем, что нам возвращается ошибка, если currentPage отсутствует.

        :return: None.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_current_page(self) -> None:
        """
        Проверяем, что нам возвращается ошибка, если currentPage невалидный.

        :return: None.
        """
        response = self.client.get(self.url, data={"currentPage": "g"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_archived_products(self) -> None:
        """
        Проверим, чтобы в выдаче не было архивированных продуктов.

        :return: None.
        """
        for product in self.sale_products:
            product.archived = True
        Product.objects.bulk_update(self.sale_products, ["archived"])
        response = self.client.get(self.url, data={"currentPage": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 0)

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
