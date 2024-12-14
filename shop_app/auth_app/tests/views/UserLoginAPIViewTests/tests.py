from copy import copy
from random import choices
from string import ascii_letters
from typing import Dict

from auth_app.tests.utils import get_user_data_from_frontend
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class UserLoginAPIViewTests(APITestCase):
    """
    Класс Тест для UserLoginAPIView.
    """

    __exists_user_data: Dict[str, str] = {
        "username": "E".join(choices(ascii_letters, k=10)),
        "password": "E".join(choices(ascii_letters, k=10)),
    }
    user: User
    url = reverse("auth_app:login")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.
        Создаём нового пользователя.

        :return: None.
        """
        super().setUpClass()
        cls.user = User.objects.create_user(**cls.__exists_user_data)

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.
        Выйдем из системы.

        :return: None.
        """
        self.user_data = copy(self.__exists_user_data)
        self.client.logout()
        # Убедимся, что пользователь не вошёл в систему перед тестами.
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_login_valid_data(self) -> None:
        """
        Тест аутентификации пользователя с валидными данными. Ожидаем статус 200 и пользователя вошедшего в систему.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        data = get_user_data_from_frontend(self.user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.session.get("_auth_user_id"), str(self.user.pk))

    def test_login_invalid_username(self) -> None:
        """
        Тест аутентификации пользователя с невалидными данными: неверный username.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        self.user_data["username"] = "N".join(choices(ascii_letters, k=10))
        data = get_user_data_from_frontend(self.user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_login_no_username(self) -> None:
        """
        Тест аутентификации пользователя с невалидными данными: username отсутствует в запросе.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        self.user_data.pop("username")
        data = get_user_data_from_frontend(self.user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_login_invalid_password(self) -> None:
        """
        Тест аутентификации пользователя с невалидными данными: неверный password.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        self.user_data["password"] = "N".join(choices(ascii_letters, k=10))
        data = get_user_data_from_frontend(self.user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.client.session.get("_auth_user_id"))

    def test_login_no_password(self) -> None:
        """
        Тест аутентификации пользователя с невалидными данными: password отсутствует в запросе.
        (Почему-то данные должны быть в такой форме:
        ключ - это словарь из данных пользователя, а значение не имеет значения,
        фронт шлёт именно так, поступим также...)

        :return: None.
        """
        self.user_data.pop("password")
        data = get_user_data_from_frontend(self.user_data)
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.client.session.get("_auth_user_id"))

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.user.delete()
        super().tearDownClass()
