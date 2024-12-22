from random import choices, randint
from string import ascii_letters

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from product_app.models import Tag, Product, SubCategory, Category, Review
from product_app.serializers.review import ReviewSerializer
from product_app.tests.utils import get_category, get_sub_category, get_simple_product


class ProductReviewsViewTests(APITestCase):
    """
    Тест ProductReviewsView
    """
    url_view_name = "product_app:product-review"
    review_serializer = ReviewSerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.category = get_category()
        cls.sub_category = get_sub_category(cls.category)
        cls.product = get_simple_product(cls.sub_category)
        cls.url = reverse(cls.url_view_name, kwargs={'product_id': cls.product.pk})

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        self.valid_data = {
            "author": "".join(choices(ascii_letters, k=6)),
            "email": f'{"".join(choices(ascii_letters, k=6))}@{"".join(choices(ascii_letters, k=6))}.com',
            "text": "".join(choices(ascii_letters, k=6)),
            "rate": randint(1, 5),
        }

    def test_valid_data(self) -> None:
        """
        Проверяем с валидными данными. Отзыв добавляется.

        :return: None.
        """
        # Убедимся, что у продукта нет отзывов.
        reviews = Review.objects.filter(product=self.product).count()
        self.assertEqual(reviews, 0)

        response: Response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reviews_after = Review.objects.filter(product=self.product)
        self.assertEqual(response.data, self.review_serializer(reviews_after, many=True).data)
        self.assertEqual(reviews_after.count(), 1)

    def test_invalid_id_product(self) -> None:
        """
        Тестируем с невалидными данными: не существующий продукт.

        :return: None.
        """
        last_product = Product.objects.all().order_by("id").last()
        bad_url = reverse(self.url_view_name, kwargs={'product_id': last_product.pk + 1})
        response: Response = self.client.post(bad_url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self) -> None:
        """
        Тестируем с невалидными данными: плохой email.
        Так как сериализаторы тоже тестируются,
        то все поля проверять не будем,
        проверим только одно поле, например email.
        Этого будет достаточно, что-бы понять,
        что включена проверка входящих данных.

        :return:
        """
        self.valid_data['email'] = ''.join(choices(ascii_letters, k=6))
        response: Response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        reviews = Review.objects.filter(product=self.product)
        self.assertEqual(reviews.count(), 0)

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