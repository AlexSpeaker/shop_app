from random import choices
from string import ascii_letters

from django.urls import reverse
from product_app.models import Category, SubCategory
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class CategoryListViewTests(APITestCase):
    """
    Тест CategoryListView
    """

    url = reverse("product_app:categories")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """

        super().setUpClass()
        cls.count_subcategory = 3

        cls.category = Category.objects.create(
            name="".join(choices(ascii_letters, k=6)),
        )
        cls.subcategories = SubCategory.objects.bulk_create(
            SubCategory(
                name="".join(choices(ascii_letters, k=6)), category=cls.category
            )
            for _ in range(cls.count_subcategory)
        )

    def test_get_category(self) -> None:
        """
        Получим список категорий.

        :return: None.
        """
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_list = response.data
        self.assertTrue(isinstance(data_list, list))
        self.assertTrue(len(data_list) == Category.objects.all().count())

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        for subcategory in cls.subcategories:
            subcategory.delete()
        cls.category.delete()
        super().tearDownClass()
