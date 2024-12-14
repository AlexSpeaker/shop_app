from pathlib import Path

from auth_app.models import Profile
from auth_app.tests.utils import get_user_with_profile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class UserProfileAvatarAPIViewTests(APITestCase):
    """
    Класс Тест для UserProfileAvatarAPIView.
    """

    __files_for_test_dir = Path(__file__).parent.parent.parent / "files_for_test"
    __valid_file_path = __files_for_test_dir / "valid_file.png"
    __no_valid_file_path = __files_for_test_dir / "no_valid_file.txt"
    url = reverse("profile_avatar")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.
        Создаём нового пользователя с профилем.
        Создаём объекты файлов для загрузки.

        :return: None.
        """
        super().setUpClass()
        cls.user = get_user_with_profile()
        with open(cls.__valid_file_path, "rb") as valid_file, open(
            cls.__no_valid_file_path, "rb"
        ) as no_valid_file:
            valid_data = valid_file.read()
            no_valid_data = no_valid_file.read()
        file_name = "test_image.png"
        cls.image_file = SimpleUploadedFile(
            name=file_name, content=valid_data, content_type="image/png"
        )
        cls.no_image_file = SimpleUploadedFile(
            name=file_name, content=no_valid_data, content_type="image/png"
        )

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.
        Входим пользователем в систему.

        :return: None.
        """
        self.client.force_authenticate(user=self.user)

    def test_valid_data(self) -> None:
        """
        Загрузим на аватарку картинку. Ожидаем статус 200, а у пользователя появился объект avatar.
        :return: None.
        """
        self.assertFalse(self.user.profile.avatar)
        response: Response = self.client.post(
            self.url, data={"avatar": self.image_file}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.profile.avatar)

    def test_valid_data_user_no_auth(self) -> None:
        """
        Загрузим на аватарку картинку, пользователь не выполнил вход.
        Ожидаем ошибку.

        :return: None.
        """
        self.assertFalse(self.user.profile.avatar)
        self.client.logout()
        response: Response = self.client.post(
            self.url, data={"avatar": self.image_file}
        )
        self.assertEqual(response.status_code // 100, 4)
        self.assertFalse(self.user.profile.avatar)

    def test_no_valid_data(self) -> None:
        """
        Загрузим на аватарку текстовый файл маскирующийся под картинку.
        Ожидаем ошибку.

        :return: None.
        """
        self.assertFalse(self.user.profile.avatar)
        response: Response = self.client.post(
            self.url, data={"avatar": self.no_image_file}
        )
        self.assertEqual(response.status_code // 100, 4)
        self.assertFalse(self.user.profile.avatar)

    def test_no_avatar(self) -> None:
        """
        Забудем передать аватарку.
        Ожидаем ошибку.

        :return: None.
        """
        self.assertFalse(self.user.profile.avatar)
        response: Response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code // 100, 4)
        self.assertFalse(self.user.profile.avatar)

    def tearDown(self) -> None:
        """
        Удаляем аватарку у пользователя.
        :return: None.
        """
        self.user.profile.avatar = None
        self.user.profile.save()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.user.profile.delete()  # Удалит так же файл картинки
        cls.user.delete()
        assert Profile.objects.count() == 0
        assert User.objects.count() == 0
        super().tearDownClass()
