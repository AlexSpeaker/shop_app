from random import choices
from string import ascii_letters

from auth_app.serializers.password import ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase


class ChangePasswordSerializerTests(APITestCase):
    """
    Класс Тест для сериализатора ChangePasswordSerializer.
    """

    serializer_class = ChangePasswordSerializer
    user: User
    __username: str = "".join(choices(ascii_letters, k=10))
    __password: str = "".join(choices(ascii_letters, k=10))

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.
        Создаём нового пользователя.

        :return: None.
        """
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=cls.__username, password=cls.__password
        )

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.
        Создаём валидный набор данных.

        :return: None.
        """
        self.valid_data = {
            "currentPassword": self.__password,
            "newPassword": "".join(choices(ascii_letters, k=10)),
        }

    def test_valid_data(self) -> None:
        """
        Тест с валидными данными. Ожидаем True от сериализатора.

        :return: None.
        """
        serializer = self.serializer_class(data=self.valid_data, instance=self.user)
        self.assertTrue(serializer.is_valid())

    def test_invalid_current_password(self) -> None:
        """
        Неверный текущий пароль.

        :return: None.
        """
        self.valid_data["currentPassword"] = "".join(choices(ascii_letters, k=15))
        serializer = self.serializer_class(data=self.valid_data, instance=self.user)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_current_password(self) -> None:
        """
        В запросе отсутствует currentPassword.

        :return: None.
        """
        self.valid_data.pop("currentPassword")
        serializer = self.serializer_class(data=self.valid_data, instance=self.user)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_data_no_new_password(self) -> None:
        """
        В запросе отсутствует newPassword.

        :return: None.
        """
        self.valid_data.pop("newPassword")
        serializer = self.serializer_class(data=self.valid_data, instance=self.user)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.user.delete()
        assert User.objects.count() == 0
        super().tearDownClass()
