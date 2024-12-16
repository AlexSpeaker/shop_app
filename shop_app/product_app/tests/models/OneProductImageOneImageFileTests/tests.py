import os
from pathlib import Path
from random import choices
from string import ascii_letters

from auth_app.tests.utils import count_files_in_directory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from product_app.models import Category, Product, ProductImage, SubCategory

from shop_app import settings


class OneProductImageOneImageFileTests(TestCase):
    """
    Тест для сигналов модели ProductImage.
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
        category = Category.objects.create(name="".join(choices(ascii_letters, k=6)))
        subcategory = SubCategory.objects.create(
            name="".join(choices(ascii_letters, k=6)), category=category
        )
        cls.product = Product.objects.create(
            title="".join(choices(ascii_letters, k=6)),
            category=subcategory,
            price=100,
            count=100,
            description="".join(choices(ascii_letters, k=16)),
        )

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        self.product_image = ProductImage.objects.create(
            title="".join(choices(ascii_letters, k=6)),
            product=self.product,
        )

        self.image_file_root = os.path.join(
            settings.MEDIA_ROOT,
            "product_image",
            str(self.product.pk),
            str(self.product_image.pk),
        )
        # Может случиться, что тестовый объект может использовать ту же папку, что и реальный,
        # по этому заранее это посчитаем.
        self.count_exist_user_files = count_files_in_directory(self.image_file_root)

        self.product_image.image = self.image_file
        self.product_image.save()

    def test_update_image(self) -> None:
        """
        Обновим картинку у ProductImage. Ожидаем в папке 1 файл.

        :return: None.
        """

        self.product_image.image = self.image_file
        self.product_image.save()
        self.assertEqual(
            count_files_in_directory(self.image_file_root),
            1 + self.count_exist_user_files,
        )

    def test_delete_image(self) -> None:
        """
        Удалим картинку у ProductImage.

        :return: None.
        """
        # Убедимся, что файл уже есть.
        self.assertEqual(
            count_files_in_directory(self.image_file_root),
            1 + self.count_exist_user_files,
        )

        self.product_image.image = None
        self.product_image.save()

        self.assertEqual(
            count_files_in_directory(self.image_file_root),
            self.count_exist_user_files,
        )

    def test_delete_product_image_obj(self) -> None:
        """
        Удалим ProductImage.

        :return: None.
        """
        # Убедимся, что файл есть.
        self.assertEqual(
            count_files_in_directory(self.image_file_root),
            1 + self.count_exist_user_files,
        )

        self.product_image.delete()

        self.assertEqual(
            count_files_in_directory(self.image_file_root),
            self.count_exist_user_files,
        )

    def tearDown(self) -> None:
        """
        Функция очищает всё после каждого теста.

        :return:
        """
        if self.product_image.pk:
            self.product_image.delete()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.product.delete()
        super().tearDownClass()
