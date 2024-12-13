from random import choices
from string import ascii_letters
from typing import Dict

from auth_app.tests.utils import get_user_data_from_frontend
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class RegisterUserAPIViewTests(APITestCase):
    """
    Класс Тест для RegisterUserAPIView.
    """

    exists_user_data: Dict[str, str] = {
        "username": "E".join(choices(ascii_letters, k=10)),
        "password": "E".join(choices(ascii_letters, k=10)),
    }
    user: User
    url = reverse("registration")

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
            "name": "N".join(choices(ascii_letters, k=10)),
        }

    def test_register_user_valid_data(self) -> None:
        """
        Тест регистрации с валидными данными. Ожидаем статус 200 и созданного пользователя.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """

        # Убедимся, что в БД есть только 1 пользователь и это пользователь,
        # которого мы создали перед тестами.
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].username, self.exists_user_data["username"])
        self.assertEqual(users[0].pk, self.user.pk)

        data = get_user_data_from_frontend(self.new_user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_user: User = User.objects.get(username=self.new_user_data["username"])
        self.assertEqual(self.client.session.get("_auth_user_id"), str(new_user.pk))
        self.assertTrue(new_user.profile is not None)
        self.assertEqual(new_user.profile.name, self.new_user_data["name"])

    def test_register_user_invalid_username_exists_username(self) -> None:
        """
        Тест регистрации с невалидными данными: существующий username.
        Ожидаем статус 400 и никакого нового пользователя.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        self.new_user_data["username"] = self.exists_user_data["username"]
        data = get_user_data_from_frontend(self.new_user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_invalid_username_less_than_four_characters(self) -> None:
        """
        Тест регистрации с невалидными данными: username меньше 4 символов.
        Ожидаем статус 400 и никакого нового пользователя.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        self.new_user_data["username"] = "abc"
        data = get_user_data_from_frontend(self.new_user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_invalid_name_less_than_two_characters(self) -> None:
        """
        Тест регистрации с невалидными данными: name меньше 2 символов.
        Ожидаем статус 400 и никакого нового пользователя.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        self.new_user_data["name"] = "a"
        data = get_user_data_from_frontend(self.new_user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_invalid_password_less_than_eight_characters(self) -> None:
        """
        Тест регистрации с невалидными данными: password меньше 8 символов.
        Ожидаем статус 400 и никакого нового пользователя.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        self.new_user_data["password"] = "abcdefg"
        data = get_user_data_from_frontend(self.new_user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.user.delete()
        super().tearDownClass()
