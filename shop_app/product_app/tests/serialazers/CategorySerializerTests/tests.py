import os
from pathlib import Path
from random import choices
from string import ascii_letters

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from product_app.models import Category, SubCategory
from product_app.serializers.categories import CategorySerializer


class CategorySerializerTests(TestCase):
    """
    Класс Тест для сериализатора CategorySerializer.
    """

    __files_for_test_dir = Path(__file__).parent.parent.parent / "files_for_test"
    __valid_file_path = __files_for_test_dir / "image.png"
    category_serializer = CategorySerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """

        super().setUpClass()
        cls.count_subcategory = 3
        cls.file_name = "test_image.png"
        with open(cls.__valid_file_path, "rb") as valid_file:
            image_file = SimpleUploadedFile(
                name=cls.file_name,
                content=valid_file.read(),
                content_type="image/png",
            )

        cls.category = Category.objects.create(
            name="".join(choices(ascii_letters, k=6)),
            image=image_file,
        )

        cls.subcategories = SubCategory.objects.bulk_create(
            SubCategory(
                name="".join(choices(ascii_letters, k=6)),
                category=cls.category,
                image=image_file,
            )
            for _ in range(cls.count_subcategory)
        )

    def test_serialize_category(self) -> None:
        """
        Проверим все ли данные на месте при получении данных.

        :return: None.
        """
        serializer = self.category_serializer(instance=self.category)
        data = serializer.data
        self.assertEqual({"id", "title", "image", "subcategories"}, set(data.keys()))
        self.assertEqual({"src", "alt"}, set(data["image"].keys()))
        self.assertTrue(
            data["image"]["src"].endswith(
                str(
                    os.path.join(str(self.category.unique_id), "images", self.file_name)
                )
            )
        )
        self.assertEqual(len(data["subcategories"]), self.count_subcategory)
        self.assertEqual({"id", "title", "image"}, set(data["subcategories"][0].keys()))
        self.assertEqual({"src", "alt"}, set(data["subcategories"][0]["image"].keys()))
        self.assertTrue(
            data["subcategories"][0]["image"]["src"].endswith(
                str(os.path.join("images", self.file_name))
            )
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        for subcategory in cls.subcategories:
            subcategory.delete()
        cls.category.delete()
        super().tearDownClass()
