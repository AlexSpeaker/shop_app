from random import choices
from string import ascii_letters
from typing import Dict

from auth_app.models import Profile
from auth_app.serializers.profile import ProfileSerializer
from auth_app.tests.utils import get_user_with_profile
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError


class ProfileSerializerTests(TestCase):
    """
    Класс Тест для сериализатора ProfileSerializer.
    """

    __name = "".join(choices(ascii_letters, k=6))
    __surname = "".join(choices(ascii_letters, k=6))
    __patronymic = "".join(choices(ascii_letters, k=6))
    __full_name = " ".join(
        [
            __surname,
            __name,
            __patronymic,
        ]
    )
    __email = "".join(["".join(choices(ascii_letters, k=10)), "@gmail.com"])
    __phone_number = "".join(choices("0123456789", k=9))

    serializer_class = ProfileSerializer
    user: User

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.
        Создаём нового пользователя с профилем.

        :return: None.
        """
        super().setUpClass()
        cls.user = get_user_with_profile()

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.
        Создаём валидный набор данных для профиля пользователя.

        :return: None.
        """
        self.valid_user_data: Dict[str, str] = {
            "fullName": self.__full_name,
            "email": self.__email,
            "phone": self.__phone_number,
        }

    def test_valid_data(self) -> None:
        """
        Тест с валидными данными. Ожидаем True от сериализатора.

        :return: None.
        """
        serializer = self.serializer_class(data=self.valid_user_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_full_name(self) -> None:
        """
        Тест с невалидными данными: невалидный fullName.

        :return: None.
        """
        self.valid_user_data["fullName"] = ""
        serializer = self.serializer_class(data=self.valid_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_no_full_name(self) -> None:
        """
        Тест с невалидными данными: fullName отсутствует.

        :return: None.
        """
        self.valid_user_data.pop("fullName")
        serializer = self.serializer_class(data=self.valid_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_email(self) -> None:
        """
        Тест с невалидными данными: невалидный email.

        :return: None.
        """
        self.valid_user_data["email"] = "".join(choices(ascii_letters, k=10))
        serializer = self.serializer_class(data=self.valid_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_no_email(self) -> None:
        """
        Тест с невалидными данными: email отсутствует.

        :return: None.
        """
        self.valid_user_data.pop("email")
        serializer = self.serializer_class(data=self.valid_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_phone(self) -> None:
        """
        Тест с невалидными данными: невалидный phone.

        :return: None.
        """
        self.valid_user_data["phone"] = "".join(choices(ascii_letters, k=10))
        serializer = self.serializer_class(data=self.valid_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_no_phone(self) -> None:
        """
        Тест с невалидными данными: phone отсутствует.

        :return: None.
        """
        self.valid_user_data.pop("phone")
        serializer = self.serializer_class(data=self.valid_user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_get_data(self) -> None:
        """
        Проверим все ли данные на месте при получении данных пользователя.

        :return: None.
        """
        serializer = self.serializer_class(instance=self.user.profile)

        # Должны быть ключи fullName, email, phone, avatar
        self.assertEqual(
            {"fullName", "email", "phone", "avatar"}, set(serializer.data.keys())
        )
        # А у avatar должны быть ключи src и alt
        self.assertEqual({"src", "alt"}, set(serializer.data["avatar"].keys()))

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.user.delete()
        assert Profile.objects.count() == 0
        assert User.objects.count() == 0
        super().tearDownClass()
