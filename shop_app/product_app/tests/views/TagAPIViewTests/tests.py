from django.urls import reverse
from product_app.models import Category, Product, SubCategory, Tag
from product_app.tests.utils import (
    get_category,
    get_simple_product,
    get_sub_category,
    get_tag,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class TagAPIViewTests(APITestCase):
    """
    Тест TagAPIView
    """

    url = reverse("product_app:tags")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.category = get_category()
        cls.sub_category = get_sub_category(cls.category)
        cls.list_products = [get_simple_product(cls.sub_category) for _ in range(20)]
        # По задумке, TagAPIView должна возвратить первые 10 тегов
        # отсортированных по количеству связанных продуктов по убыванию.
        # Создадим 20 тегов.
        cls.tags_list = [get_tag() for _ in range(20)]
        # Сделаем, чтобы у 1-го в списке тегов было больше всего связанных продуктов,
        # у второго чуть поменьше и т.д.
        for i in range(20):
            cls.tags_list[i].products.add(*cls.list_products[: 20 - i])
            cls.tags_list[i].save()

    def test_get_tags_no_valid_params(self) -> None:
        """
        Проверим, что TagAPIView возвращает ошибку, если переданные параметры не верные.

        :return: None.
        """
        response: Response = self.client.get(self.url, data={"category": "s"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_tags(self) -> None:
        """
        Проверим, что TagAPIView возвращает то, что от неё ожидаем.

        :return: None.
        """
        response: Response = self.client.get(
            self.url, data={"category": self.sub_category.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tags_id_list = [tag.pk for tag in self.tags_list[:10]]
        response_tags_id_list = [tag["id"] for tag in response.data]
        self.assertEqual(tags_id_list, response_tags_id_list)

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
