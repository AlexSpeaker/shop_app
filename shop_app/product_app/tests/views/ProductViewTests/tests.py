from random import choice

from django.urls import reverse
from product_app.models import Category, Product, SubCategory, Tag
from product_app.serializers.product import OutProductSerializer
from product_app.tests.utils import get_product
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class ProductViewTests(APITestCase):
    """
    Тест ProductView
    """

    url_view_name = "product_app:product"
    product_serializer = OutProductSerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.list_products = [get_product(), get_product()]

    def test_get_product(self) -> None:
        """
        Проверяем получение детальной информации о продукте.

        :return:
        """
        for product in self.list_products:
            url = reverse(self.url_view_name, kwargs={"product_id": product.pk})

            response: Response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            serializer = OutProductSerializer(product)
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.data["id"], product.pk)

    def test_product_reviews(self) -> None:
        """
        Проверяем, что отзыв принадлежит продукту.
        Мы точно знаем, что у одного продукта - один отзыв.

        :return: None.
        """
        product = choice(self.list_products)
        url = reverse(self.url_view_name, kwargs={"product_id": product.pk})
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["reviews"][0]["author"], product.reviews.all()[0].author
        )
        self.assertEqual(len(response.data["reviews"]), product.reviews.all().count())

    def test_product_specifications(self) -> None:
        """
        Проверяем, что спецификация принадлежит продукту.
        Мы точно знаем, что у одного продукта - одна спецификация.

        :return: None.
        """
        product = choice(self.list_products)
        url = reverse(self.url_view_name, kwargs={"product_id": product.pk})
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["specifications"][0]["name"],
            product.specifications.all()[0].name,
        )
        self.assertEqual(
            len(response.data["specifications"]), product.specifications.all().count()
        )

    def test_product_tags(self) -> None:
        """
        Проверяем, что тег принадлежит продукту.
        Мы точно знаем, что у одного продукта - один тег.

        :return: None.
        """
        product = choice(self.list_products)
        url = reverse(self.url_view_name, kwargs={"product_id": product.pk})
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tags"][0]["name"], product.tags.all()[0].name)
        self.assertEqual(len(response.data["tags"]), product.tags.all().count())

    def test_archived_product(self) -> None:
        """
        Проверяем с архивированным продуктом.

        :return:
        """
        product = choice(self.list_products)
        product.archived = True
        product.save()
        url = reverse(self.url_view_name, kwargs={"product_id": product.pk})
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        product.archived = False
        product.save()

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
