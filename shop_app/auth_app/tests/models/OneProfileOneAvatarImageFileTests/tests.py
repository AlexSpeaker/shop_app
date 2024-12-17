import os.path
from pathlib import Path

from auth_app.tests.utils import count_files_in_directory, get_user_with_profile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from shop_app import settings


class OneProfileOneAvatarImageFileTests(TestCase):
    """
    Тест для сигналов модели Profile.
    """

    __files_for_test_dir = Path(__file__).parent.parent.parent / "files_for_test"
    __valid_file_path = __files_for_test_dir / "valid_file.png"

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        with open(cls.__valid_file_path, "rb") as valid_file:
            cls.image_file = SimpleUploadedFile(
                name="test_image.png",
                content=valid_file.read(),
                content_type="image/png",
            )

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """

        self.user = get_user_with_profile()
        self.image_file_root = os.path.join(
            settings.MEDIA_ROOT, "profile", str(self.user.profile.unique_id), "avatar"
        )
        self.user.profile.avatar = self.image_file
        self.user.profile.save()

    def test_update_avatar(self) -> None:
        """
        Обновим аватарку у пользователя. Ожидаем в папке 1 файл.

        :return: None.
        """
        self.user.profile.avatar = self.image_file
        self.user.profile.save()
        self.assertEqual(count_files_in_directory(self.image_file_root), 1)

    def test_delete_avatar(self) -> None:
        """
        Удалим аватар у пользователя.

        :return: None.
        """
        # Убедимся, что файл аватарки уже есть.
        self.assertEqual(count_files_in_directory(self.image_file_root), 1)

        self.user.profile.avatar = None
        self.user.profile.save()

        self.assertEqual(count_files_in_directory(self.image_file_root), 0)

    def test_delete_user(self) -> None:
        """
        Удалим пользователя.

        :return: None.
        """
        # Убедимся, что файл аватарки уже есть.
        self.assertEqual(count_files_in_directory(self.image_file_root), 1)

        self.user.delete()

        self.assertEqual(count_files_in_directory(self.image_file_root), 0)

    def test_delete_many_users(self) -> None:
        """
        Попробуем удалить несколько пользователей сразу.

        :return: None.
        """
        users = [get_user_with_profile() for _ in range(5)]
        image_file_roots = [
            os.path.join(
                settings.MEDIA_ROOT, "profile", str(user.profile.unique_id), "avatar"
            )
            for user in users
        ]

        for user in users:
            user.profile.avatar = self.image_file
            user.profile.save()

        # Убедимся, что файлы есть:
        for image_file_root in image_file_roots:
            self.assertEqual(count_files_in_directory(image_file_root), 1)
        # Получаем из БД всех пользователей и удаляем.
        users_in_db = User.objects.all()
        users_in_db.delete()

        # Убедимся, что файлы удалены.
        for image_file_root in image_file_roots:
            self.assertEqual(count_files_in_directory(image_file_root), 0)

    def tearDown(self) -> None:
        """
        Функция очищает всё после каждого теста.

        :return:
        """
        if self.user.pk:
            self.user.delete()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        super().tearDownClass()
