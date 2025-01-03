from random import choices
from string import ascii_letters

from django.test import TestCase
from product_app.models import Tag
from product_app.serializers.tag import OutTagSerializer


class OutTagSerializerTests(TestCase):
    """
    Класс Тест для сериализатора OutTagSerializer.
    """

    tag_serializer = OutTagSerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """

        super().setUpClass()
        cls.tag = Tag.objects.create(name="".join(choices(ascii_letters, k=6)))

    def test_tag_data(self) -> None:
        serializer = self.tag_serializer(self.tag)
        self.assertEqual({"name", "id"}, set(serializer.data.keys()))
        self.assertEqual(serializer.data["name"], self.tag.name)
        self.assertEqual(serializer.data["id"], self.tag.id)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        cls.tag.delete()
        super().tearDownClass()
