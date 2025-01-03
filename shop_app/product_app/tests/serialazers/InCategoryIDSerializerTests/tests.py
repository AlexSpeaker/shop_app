from typing import Any, Dict

from django.test import TestCase
from product_app.serializers.category import InCategoryIDSerializer
from rest_framework.exceptions import ValidationError


class InCategoryIDSerializerTests(TestCase):
    """
    Класс Тест для сериализатора InCategoryIDSerializer.
    """

    category_id_serializer = InCategoryIDSerializer

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        self.valid_data: Dict[str, Any] = dict()
        self.valid_data["category_id"] = 1

    def test_valid_data(self) -> None:
        """
        Тест с валидными данными.

        :return: None.
        """

        serializer = self.category_id_serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.valid_data["category_id"] = "1"
        serializer_str = self.category_id_serializer(data=self.valid_data)
        self.assertTrue(serializer_str.is_valid())

    def test_invalid_data_bad_category_id(self) -> None:
        """
        Тестируем невалидные данные: плохой category_id.

        :return: None.
        """
        bad_data_list = ["", -1, "a", 0]
        for bad_category_id in bad_data_list:
            self.valid_data["category_id"] = bad_category_id
            serializer = self.category_id_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_category_id(self) -> None:
        """
        Тестируем невалидные данные: нет category_id.

        :return: None.
        """
        self.valid_data.pop("category_id")
        serializer = self.category_id_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
