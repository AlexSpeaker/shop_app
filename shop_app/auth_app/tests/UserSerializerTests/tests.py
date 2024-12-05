from random import choices
from string import ascii_letters
from typing import Dict

from auth_app.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase


class UserSerializerTests(APITestCase):
    """
    Класс Тест для сериализатора UserSerializer.
    """

    serializer_class = UserSerializer
    exists_user_data: Dict[str, str] = {
        "username": "E".join(choices(ascii_letters, k=10)),
        "password": "E".join(choices(ascii_letters, k=10)),
        "first_name": "E".join(choices(ascii_letters, k=10)),
    }
    user: User

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.
        Создаём нового пользователя.

        :return: None.
        """
        super().setUpClass()
        cls.user = User.objects.create_user(**cls.exists_user_data)

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.
        Создаём валидный набор данных для создания пользователя.

        :return: None.
        """
        self.new_user_data: Dict[str, str] = {
            "username": "N".join(choices(ascii_letters, k=10)),
            "password": "N".join(choices(ascii_letters, k=10)),
            "first_name": "N".join(choices(ascii_letters, k=10)),
        }

    def test_valid_data(self) -> None:
        """
        Тест с валидными данными. Ожидаем True от сериализатора.

        :return: None.
        """
        serializer = self.serializer_class(data=self.new_user_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_username_exists_username(self) -> None:
        """
        Тест с невалидными данными: существующий username.

        :return: None.
        """
        self.new_user_data["username"] = self.exists_user_data["username"]
        serializer = self.serializer_class(data=self.new_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_username_less_than_six_characters(self) -> None:
        """
        Тест с невалидными данными: username меньше 6 символов.

        :return: None.
        """
        self.new_user_data["username"] = "abcde"
        serializer = self.serializer_class(data=self.new_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_first_name_less_than_two_characters(self) -> None:
        """
        Тест с невалидными данными: first_name меньше 2 символов.

        :return: None.
        """
        self.new_user_data["first_name"] = "a"
        serializer = self.serializer_class(data=self.new_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_password_less_than_eight_characters(self) -> None:
        """
        Тест с невалидными данными: password меньше 8 символов.

        :return: None.
        """
        self.new_user_data["password"] = "abcdefg"
        serializer = self.serializer_class(data=self.new_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.user.delete()
        super().tearDownClass()
