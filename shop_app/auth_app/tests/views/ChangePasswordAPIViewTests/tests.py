from random import choices
from string import ascii_letters
from typing import Dict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class ChangePasswordAPIViewTests(APITestCase):
    """
    Класс Тест для ChangePasswordAPIView.
    """

    __exists_user_data: Dict[str, str] = {
        "username": "".join(choices(ascii_letters, k=10)),
        "password": "".join(choices(ascii_letters, k=10)),
    }
    user: User
    url = reverse("profile_password")

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
        Создаём валидный набор данных для смены пароля пользователя.

        :return: None.
        """
        self.valid_data = {
            "currentPassword": self.__exists_user_data["password"],
            "newPassword": "".join(choices(ascii_letters, k=10)),
        }
        self.client.force_authenticate(user=self.user)

    def test_valid_data(self) -> None:
        """
        Тест с валидными данными. Ожидаем статус 200 и новый пароль у пользователя.

        :return: None.
        """
        response: Response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(self.valid_data["newPassword"]))

    def test_valid_data_no_auth_user(self) -> None:
        """
        Тест с валидными данными. Пользователь не вошёл в систему. Ожидаем ошибку.

        :return: None.
        """
        self.client.logout()
        response: Response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code // 100, 4)
        self.assertTrue(self.user.check_password(self.valid_data["currentPassword"]))

    def test_invalid_current_password(self) -> None:
        """
        Неверный текущий пароль.

        :return: None.
        """
        password: str = self.valid_data["currentPassword"]
        self.valid_data["currentPassword"] = "".join(choices(ascii_letters, k=10))
        response: Response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code // 100, 4)
        self.assertTrue(self.user.check_password(password))

    def test_invalid_data_no_current_password(self) -> None:
        """
        В запросе отсутствует currentPassword.

        :return: None.
        """
        password = self.valid_data.pop("currentPassword")
        response: Response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code // 100, 4)
        self.assertTrue(self.user.check_password(password))

    def test_invalid_data_no_new_password(self) -> None:
        """
        В запросе отсутствует newPassword.

        :return: None.
        """
        self.valid_data.pop("newPassword")
        response: Response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code // 100, 4)
        self.assertTrue(self.user.check_password(self.valid_data["currentPassword"]))

    def tearDown(self) -> None:
        """
        Возвращаем пароль пользователю по умолчанию.

        :return: None.
        """
        self.user.set_password(self.__exists_user_data["password"])

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.user.delete()
        super().tearDownClass()
