from datetime import timedelta

from django.core.paginator import Paginator
from django.test import TestCase
from django.utils import timezone
from product_app.models import Product, Sale
from product_app.serializers.catalog import OutCatalogSalesSerializer
from product_app.tests.utils import get_product


class OutCatalogSalesSerializerTests(TestCase):
    """
    Класс Тест для сериализатора OutCatalogSalesSerializer.
    """

    sale_serializer = OutCatalogSalesSerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.product_1 = get_product()
        cls.product_2 = get_product()
        cls.sale_2 = Sale.objects.create(
            product=cls.product_2,
            date_from=timezone.now().date(),
            date_to=timezone.now().date() + timedelta(days=1),
            price=cls.product_2.price + 100,
            sale_price=1,
        )
        cls.sale_1 = Sale.objects.create(
            product=cls.product_1,
            date_from=timezone.now().date(),
            date_to=timezone.now().date() + timedelta(days=1),
            price=cls.product_1.price + 200,
            sale_price=1,
        )

    def test_serialize(self) -> None:
        """
        Проверяем: все ли поля на месте.

        :return: None.
        """
        limit = 10
        current_page = 1
        sales = Sale.objects.select_related("product").all().order_by("product__id")
        paginator = Paginator(sales, limit)
        page_odj = paginator.get_page(current_page)
        serializer = self.sale_serializer(page_odj)
        data = serializer.data
        set_sale_keys = {
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images",
        }
        self.assertEqual(set_sale_keys, set(data["items"][0].keys()))
        set_keys = {"items", "currentPage", "lastPage"}
        self.assertEqual(set_keys, set(data.keys()))
        self.assertEqual(data["items"][0]['id'], self.product_1.id)
        self.assertAlmostEqual(float(data["items"][0]['price']), self.sale_1.price, places=2)
        self.assertAlmostEqual(float(data["items"][0]['salePrice']), self.sale_1.sale_price, places=2)
        self.assertEqual(data["items"][0]['dateFrom'], self.sale_1.date_from.strftime("%m-%d"))
        self.assertEqual(data["items"][0]['dateTo'], self.sale_1.date_to.strftime("%m-%d"))
        self.assertEqual(data["items"][0]['title'], self.product_1.title)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Функция очищает всё после всех тестов.

        :return: None.
        """
        Product.objects.all().delete()
        super().tearDownClass()
