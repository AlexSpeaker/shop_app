from random import choices
from string import ascii_letters
from typing import Any, Dict, Never

from django.test import TestCase
from product_app.serializers.catalog import InCatalogSerializer
from rest_framework.exceptions import ValidationError


class InCatalogSerializerTests(TestCase):
    """
    Класс Тест для сериализатора InCatalogSerializer.
    """

    in_catalog_serializer = InCatalogSerializer

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        self.valid_data: Dict[str, Any] = dict()
        self.filter: Dict[str, Any] = dict()
        self.valid_data["filter"] = self.filter

        self.filter["name"] = "".join(choices(ascii_letters, k=6))
        self.filter["minPrice"] = 1
        self.filter["maxPrice"] = 100
        self.filter["freeDelivery"] = True
        self.filter["available"] = True

        self.valid_data["currentPage"] = 1
        self.valid_data["category"] = 1
        self.valid_data["sort"] = "price"
        self.valid_data["sortType"] = "inc"
        self.valid_data["limit"] = 1
        self.valid_data["tags"] = [1, 2, 3]

    def test_valid_data(self) -> None:
        """
        Тест с валидными данными.

        :return: None.
        """
        serializer = self.in_catalog_serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_valid_data_optionally_sort(self) -> None:
        """
        Тест с валидными данными более детально: sort.

        :return: None.
        """
        sort_valid_data = ["rating", "price", "reviews", "date"]
        for item in sort_valid_data:
            self.valid_data["sort"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            self.assertTrue(serializer.is_valid())

    def test_valid_data_optionally_sort_type(self) -> None:
        """
        Тест с валидными данными более детально: sortType.

        :return: None.
        """
        sort_type_valid_data = ["inc", "dec"]
        for item in sort_type_valid_data:
            self.valid_data["sortType"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            self.assertTrue(serializer.is_valid())

    def test_valid_data_optionally_tags(self) -> None:
        """
        Тест с валидными данными более детально: tags.

        :return: None.
        """
        self.valid_data.pop("tags")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_bad_current_page(self) -> None:
        """
        Тестируем невалидные данные: плохой currentPage.

        :return: None.
        """
        current_page_invalid_data = ["a", 0, -1]
        for item in current_page_invalid_data:
            self.valid_data["currentPage"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_current_page(self) -> None:
        """
        Тестируем невалидные данные: нет currentPage.

        :return: None.
        """
        self.valid_data.pop("currentPage")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_category(self) -> None:
        """
        Тестируем невалидные данные: плохой category.

        :return: None.
        """
        category_invalid_data = ["a", 0, -1]
        for item in category_invalid_data:
            self.valid_data["category"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_sort(self) -> None:
        """
        Тестируем невалидные данные: плохой sort.

        :return: None.
        """
        sort_invalid_data = ["a", 1]
        for item in sort_invalid_data:
            self.valid_data["sort"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_sort(self) -> None:
        """
        Тестируем невалидные данные: нет sort.

        :return: None.
        """
        self.valid_data.pop("sort")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_sort_type(self) -> None:
        """
        Тестируем невалидные данные: плохой sortType.

        :return: None.
        """
        sort_type_invalid_data = ["a", 1]
        for item in sort_type_invalid_data:
            self.valid_data["sortType"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_sort_type(self) -> None:
        """
        Тестируем невалидные данные: нет sortType.

        :return: None.
        """
        self.valid_data.pop("sortType")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_limit(self) -> None:
        """
        Тестируем невалидные данные: плохой limit.

        :return: None.
        """
        limit_invalid_data = ["a", 0, -1]
        for item in limit_invalid_data:
            self.valid_data["limit"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_limit(self) -> None:
        """
        Тестируем невалидные данные: нет limit.

        :return: None.
        """
        self.valid_data.pop("limit")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_tags(self) -> None:
        """
        Тестируем невалидные данные: плохой tags.

        :return: None.
        """
        tags_invalid_data: tuple[list[int], list[object], list[int], list[Never]] = (
            [1, 2, -1],
            ["a", 1, 2],
            [0, 1, 2],
            [],
        )
        for item in tags_invalid_data:
            self.valid_data["tags"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_name(self) -> None:
        """
        Тестируем невалидные данные: нет name.

        :return: None.
        """
        self.filter.pop("name")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_min_price(self) -> None:
        """
        Тестируем невалидные данные: плохой minPrice.

        :return: None.
        """
        min_price_invalid_data = ["a", -1]
        for item in min_price_invalid_data:
            self.filter["minPrice"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_min_price(self) -> None:
        """
        Тестируем невалидные данные: нет minPrice.

        :return: None.
        """
        self.filter.pop("minPrice")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_max_price(self) -> None:
        """
        Тестируем невалидные данные: плохой maxPrice.

        :return: None.
        """
        max_price_invalid_data = ["a", -1]
        for item in max_price_invalid_data:
            self.filter["maxPrice"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_max_price(self) -> None:
        """
        Тестируем невалидные данные: нет maxPrice.

        :return: None.
        """
        self.filter.pop("maxPrice")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_max_price_and_min_price(self) -> None:
        """
        Тестируем невалидные данные: maxPrice < minPrice.

        :return: None.
        """
        self.filter["maxPrice"] = 100
        self.filter["minPrice"] = 200
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_free_delivery(self) -> None:
        """
        Тестируем невалидные данные: плохой freeDelivery.

        :return: None.
        """
        free_delivery_invalid_data = ["a", 2, -1]
        for item in free_delivery_invalid_data:
            self.filter["freeDelivery"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_free_delivery(self) -> None:
        """
        Тестируем невалидные данные: нет freeDelivery.

        :return: None.
        """
        self.filter.pop("freeDelivery")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_bad_available(self) -> None:
        """
        Тестируем невалидные данные: плохой available.

        :return: None.
        """
        available_invalid_data = ["a", 2, -1]
        for item in available_invalid_data:
            self.filter["available"] = item
            serializer = self.in_catalog_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_available(self) -> None:
        """
        Тестируем невалидные данные: нет available.

        :return: None.
        """
        self.filter.pop("available")
        serializer = self.in_catalog_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
