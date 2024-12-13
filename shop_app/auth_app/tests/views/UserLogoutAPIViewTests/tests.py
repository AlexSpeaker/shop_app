from random import choices
from string import ascii_letters
from typing import Dict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class UserLogoutAPIViewTests(APITestCase):
    """
    Класс Тест для UserLogoutAPIView.
    """

    exists_user_data: Dict[str, str] = {
        "username": "E".join(choices(ascii_letters, k=10)),
        "password": "E".join(choices(ascii_letters, k=10)),
    }
    user: User
    url = reverse("logout")

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
        Войдём созданным пользователем в систему.

        :return: None.
        """
        self.client.login(**self.exists_user_data)

    def test_logout(self) -> None:
        """
        Тест выхода пользователя из системы.

        :return: None.
        """

        # Убедимся, что пользователь выполнил вход в систему.

        self.assertTrue(self.client.session.get("_auth_user_id"))
        self.assertEqual(self.client.session.get("_auth_user_id"), str(self.user.pk))

        response: Response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.client.session.get("_auth_user_id"))

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.user.delete()
        super().tearDownClass()
