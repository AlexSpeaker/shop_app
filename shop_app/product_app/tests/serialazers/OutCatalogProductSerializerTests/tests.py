from django.test import TestCase
from product_app.models import Category, Product, SubCategory, Tag
from product_app.serializers.product import OutCatalogProductSerializer
from product_app.tests.utils import get_product


class OutCatalogProductSerializerTests(TestCase):
    """
    Класс Тест для сериализатора OutCatalogProductSerializer.
    """

    product_serializer = OutCatalogProductSerializer

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
            .prefetch_related("tags", "images", "reviews", "sales", "specifications")
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
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        }
        self.assertEqual(set_keys, set(data.keys()))

        set_images_keys = {"src", "alt"}
        self.assertEqual(set_images_keys, set(data["images"][0].keys()))

        set_tags_keys = {"id", "name"}
        self.assertEqual(set_tags_keys, set(data["tags"][0].keys()))

        self.assertTrue(isinstance(data["reviews"], int))

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
