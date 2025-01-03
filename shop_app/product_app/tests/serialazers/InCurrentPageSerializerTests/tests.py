from typing import Any, Dict

from django.test import TestCase
from product_app.serializers.catalog import InCurrentPageSerializer
from rest_framework.exceptions import ValidationError


class InCurrentPageSerializerTests(TestCase):
    """
    Класс Тест для сериализатора InCurrentPageSerializer.
    """

    current_page_serializer = InCurrentPageSerializer

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        self.valid_data: Dict[str, Any] = dict()
        self.valid_data["currentPage"] = 1

    def test_valid_data(self) -> None:
        """
        Тест с валидными данными.

        :return: None.
        """

        serializer = self.current_page_serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_bad_current_page(self) -> None:
        """
        Тестируем невалидные данные: плохой current_page.

        :return: None.
        """
        bad_data_list = ["", -1, "a", 0]
        for current_page in bad_data_list:
            self.valid_data["currentPage"] = current_page
            serializer = self.current_page_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_current_page(self) -> None:
        """
        Тестируем невалидные данные: нет current_page.

        :return: None.
        """
        self.valid_data.pop("currentPage")
        serializer = self.current_page_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
