from random import choices, randint
from string import ascii_letters

from django.db.models import Q
from django.test import TestCase
from django.utils.timezone import get_current_timezone, now
from product_app.models import Category, Product, Review, SubCategory, Tag
from product_app.serializers.review import ReviewSerializer
from product_app.tests.utils import get_product
from rest_framework.exceptions import ValidationError


class ReviewSerializerTests(TestCase):
    """
    Класс Тест для сериализатора ReviewSerializer.
    """

    review_serializer = ReviewSerializer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.product = get_product()
        cls.review = Review.objects.create(
            product=cls.product,
            author="".join(choices(ascii_letters, k=6)),
            email=f'{"".join(choices(ascii_letters, k=6))}@{"".join(choices(ascii_letters, k=6))}.com',
            text="".join(choices(ascii_letters, k=1000)),
            rate=randint(1, 5),
            date=now(),
        )

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        self.valid_data = {
            "author": "".join(choices(ascii_letters, k=6)),
            "email": f'{"V".join(choices(ascii_letters, k=6))}@{"".join(choices(ascii_letters, k=6))}.com',
            "text": "".join(choices(ascii_letters, k=1000)),
            "rate": randint(1, 5),
            "date": now().strftime("%Y-%m-%d %H:%M"),
        }

    def test_get_data(self) -> None:
        """
        Проверяем: все ли поля на месте.

        :return: None.
        """
        serializer = self.review_serializer(self.review)
        data = serializer.data
        self.assertEqual({"author", "email", "text", "rate", "date"}, set(data.keys()))

    def test_validate_data(self) -> None:
        """
        Тест с валидными данными. Ожидаем True от сериализатора.

        :return: None.
        """
        serializer = self.review_serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        data = dict(**serializer.data, product=self.product)
        serializer.create(data)
        review = Review.objects.filter(
            Q(author=data["author"]) & Q(email=data["email"])
        ).first()
        self.assertTrue(review)

        self.assertEqual(review.author, self.valid_data["author"])
        self.assertEqual(review.email, self.valid_data["email"])
        self.assertEqual(review.text, self.valid_data["text"])
        self.assertEqual(review.rate, self.valid_data["rate"])
        local_review_date = review.date.astimezone(get_current_timezone())
        self.assertEqual(
            local_review_date.strftime("%Y-%m-%d %H:%M"), self.valid_data["date"]
        )

    def test_no_valid_data_no_author(self) -> None:
        """
        Тестируем невалидные данные: нет автора.

        :return: None.
        """
        self.valid_data.pop("author")
        serializer = self.review_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_valid_data_bad_email(self) -> None:
        """
        Тестируем невалидные данные: плохой email.

        :return: None.
        """
        self.valid_data["email"] = "".join(choices(ascii_letters, k=6))
        serializer = self.review_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_valid_data_no_email(self) -> None:
        """
        Тестируем невалидные данные: нет email.

        :return: None.
        """
        self.valid_data.pop("email")
        serializer = self.review_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_valid_data_bad_text(self) -> None:
        """
        Тестируем невалидные данные: плохой text.

        :return: None.
        """
        text_data = ("".join(choices(ascii_letters, k=5001)), "")
        for data in text_data:
            self.valid_data["text"] = data
            serializer = self.review_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_no_valid_data_no_text(self) -> None:
        """
        Тестируем невалидные данные: нет text.

        :return: None.
        """
        self.valid_data.pop("text")
        serializer = self.review_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_valid_data_bad_rate(self) -> None:
        """
        Тестируем невалидные данные: плохой rate.

        :return: None.
        """
        rate_data = ("f", "", 0, 6, 2.5)
        for data in rate_data:
            self.valid_data["rate"] = data
            serializer = self.review_serializer(data=self.valid_data)
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)

    def test_no_valid_data_no_rate(self) -> None:
        """
        Тестируем невалидные данные: нет rate.

        :return: None.
        """
        self.valid_data.pop("rate")
        serializer = self.review_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_valid_data_bad_date(self) -> None:
        """
        Тестируем невалидные данные: плохой date.

        :return: None.
        """
        self.valid_data["date"] = "".join(choices(ascii_letters, k=6))
        serializer = self.review_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_valid_data_no_date(self) -> None:
        """
        Тестируем невалидные данные: нет date.

        :return: None.
        """
        self.valid_data.pop("date")
        serializer = self.review_serializer(data=self.valid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

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
