import os
from pathlib import Path
from random import choices
from string import ascii_letters

from auth_app.tests.utils import count_files_in_directory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from product_app.models import Category, SubCategory

from shop_app import settings


class OneSubCategoryOneImageFileTests(TestCase):
    """
    Тест для сигналов модели SubCategory.
    """

    __files_for_test_dir = Path(__file__).parent.parent.parent / "files_for_test"
    __valid_file_path = __files_for_test_dir / "image.png"

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
        cls.category = Category.objects.create(
            name="".join(choices(ascii_letters, k=6))
        )

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        self.subcategory = SubCategory.objects.create(
            name="".join(choices(ascii_letters, k=6)),
            category=self.category,
            image=self.image_file,
        )

        self.image_file_root = os.path.join(
            settings.MEDIA_ROOT,
            "subcategories",
            str(self.subcategory.unique_id),
            "images",
        )

    def test_update_image(self) -> None:
        """
        Обновим картинку у подкатегории. Ожидаем в папке 1 файл.

        :return: None.
        """

        self.subcategory.image = self.image_file
        self.subcategory.save()
        self.assertEqual(count_files_in_directory(self.image_file_root), 1)

    def test_delete_image(self) -> None:
        """
        Удалим картинку у подкатегории.

        :return: None.
        """
        # Убедимся, что файл уже есть.
        self.assertEqual(count_files_in_directory(self.image_file_root), 1)

        self.subcategory.image = None
        self.subcategory.save()

        self.assertEqual(count_files_in_directory(self.image_file_root), 0)

    def test_delete_subcategory(self) -> None:
        """
        Удалим подкатегорию.

        :return: None.
        """
        # Убедимся, что файл есть.
        self.assertEqual(count_files_in_directory(self.image_file_root), 1)

        self.subcategory.delete()

        self.assertEqual(count_files_in_directory(self.image_file_root), 0)

    def tearDown(self) -> None:
        """
        Функция очищает всё после каждого теста.

        :return:
        """
        if self.subcategory.pk:
            self.subcategory.delete()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.category.delete()
        super().tearDownClass()
