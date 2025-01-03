from django.test import TestCase
from product_app.models import Category, Product, SubCategory, Tag
from product_app.serializers.product import OutProductSerializer
from product_app.tests.utils import get_product


class OutProductSerializerTests(TestCase):
    """
    Класс Тест для сериализатора OutProductSerializer.
    """

    product_serializer = OutProductSerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.product = get_product()

    def test_get_product_data(self) -> None:
        """
        Проверяем: все ли поля на месте.

        :return: None.
        """
        product: Product = (
            Product.objects.select_related("category")
            .prefetch_related("tags", "images", "specifications", "reviews")
            .all()
            .first()
        )
        serializer = self.product_serializer(product)
        data = serializer.data
        set_keys = {
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        }
        self.assertEqual(set_keys, set(data.keys()))

        set_images_keys = {"src", "alt"}
        self.assertEqual(set_images_keys, set(data["images"][0].keys()))

        set_specifications_keys = {"name", "value"}
        self.assertEqual(set_specifications_keys, set(data["specifications"][0].keys()))

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        Tag.objects.all().delete()
        Product.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()
        super().tearDownClass()
