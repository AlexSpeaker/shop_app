import os
from pathlib import Path
from random import choices
from string import ascii_letters
from typing import Dict

from auth_app.models import Profile
from auth_app.tests.utils import get_user_with_profile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class UserProfileAPIViewTests(APITestCase):
    """
    Класс Тест для UserProfileAPIView.
    """

    __files_for_test_dir = Path(__file__).parent.parent.parent / "files_for_test"
    __valid_file_path = __files_for_test_dir / "valid_file.png"
    name = "".join(choices(ascii_letters, k=6))
    surname = "".join(choices(ascii_letters, k=6))
    patronymic = "".join(choices(ascii_letters, k=6))
    full_name = " ".join(
        [
            surname,
            name,
            patronymic,
        ]
    )
    email = "".join(["".join(choices(ascii_letters, k=10)), "@gmail.com"])
    phone_number = "".join(choices("0123456789", k=9))
    url = reverse("auth_app:profile")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.
        Создаём нового пользователя с профилем.

        :return: None.
        """
        super().setUpClass()
        cls.user = get_user_with_profile()
        with open(cls.__valid_file_path, "rb") as file:
            data = file.read()
        cls.file_name = "test_image.png"
        image_file = SimpleUploadedFile(
            name=cls.file_name, content=data, content_type="image/png"
        )
        cls.user.profile.avatar = image_file
        cls.user.profile.save()

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.
        Создаём валидный набор данных для профиля пользователя.

        :return: None.
        """
        self.valid_user_data: Dict[str, str] = {
            "fullName": self.full_name,
            "email": self.email,
            "phone": self.phone_number,
        }
        self.client.force_authenticate(user=self.user)

    def test_get_auth_user_profile(self) -> None:
        """
        Пробуем получить данные пользователя вошедшего в систему.

        :return: None.
        """
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {"fullName", "email", "phone", "avatar"}, set(response.data.keys())
        )
        self.assertEqual({"src", "alt"}, set(response.data["avatar"].keys()))
        self.assertEqual(
            response.data["fullName"],
            " ".join(
                [
                    self.user.profile.surname,
                    self.user.profile.name,
                    self.user.profile.patronymic,
                ]
            ).strip(),
        )
        self.assertEqual(response.data["email"], self.user.profile.email)
        self.assertEqual(response.data["phone"], self.user.profile.phone)
        self.assertTrue(
            response.data["avatar"]["src"].endswith(
                str(
                    os.path.join(
                        str(self.user.profile.unique_id), "avatar", self.file_name
                    )
                )
            )
        )

    def test_get_no_auth_user_profile(self) -> None:
        """
        Пробуем получить данные пользователя не вошедшего в систему.

        :return: None.
        """
        self.client.logout()
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code // 100, 4)

    def test_post_auth_user_profile_valid_data(self) -> None:
        """
        Обновим профиль валидными данными у пользователя вошедшего в систему.

        :return: None.
        """
        response: Response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.user.profile.name, self.name)
        self.assertEqual(self.user.profile.surname, self.surname)
        self.assertEqual(self.user.profile.patronymic, self.patronymic)
        self.assertEqual(self.user.profile.email, self.email)
        self.assertEqual(self.user.profile.phone, self.phone_number)

    def test_post_no_auth_user_profile_valid_data(self) -> None:
        """
        Обновим профиль валидными данными у пользователя не вошедшего в систему.

        :return: None.
        """
        self.client.logout()
        response: Response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(response.status_code // 100, 4)

    def test_post_auth_user_profile_invalid_full_name(self) -> None:
        """
        Тест обновления профиля с невалидными данными: пустой fullName.

        :return: None.
        """
        self.valid_user_data["fullName"] = ""
        response: Response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(response.status_code // 100, 4)

    def test_post_auth_user_profile_no_full_name(self) -> None:
        """
        Тест обновления профиля с невалидными данными: fullName отсутствует.

        :return: None.
        """
        self.valid_user_data.pop("fullName")
        response: Response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(response.status_code // 100, 4)

    def test_post_auth_user_profile_invalid_email(self) -> None:
        """
        Тест обновления профиля с невалидными данными: плохой email.

        :return: None.
        """
        self.valid_user_data["email"] = "".join(choices(ascii_letters, k=6))
        response: Response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(response.status_code // 100, 4)

    def test_post_auth_user_profile_no_email(self) -> None:
        """
        Тест обновления профиля с невалидными данными: email отсутствует.

        :return: None.
        """
        self.valid_user_data.pop("email")
        response: Response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(response.status_code // 100, 4)

    def test_post_auth_user_profile_invalid_phone(self) -> None:
        """
        Тест обновления профиля с невалидными данными: плохой phone.

        :return: None.
        """
        self.valid_user_data["phone"] = "".join(choices(ascii_letters, k=6))
        response: Response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(response.status_code // 100, 4)

    def test_post_auth_user_profile_no_phone(self) -> None:
        """
        Тест обновления профиля с невалидными данными: phone отсутствует.

        :return: None.
        """
        self.valid_user_data.pop("phone")
        response: Response = self.client.post(self.url, data=self.valid_user_data)
        self.assertEqual(response.status_code // 100, 4)

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
