import random
from typing import Any, Dict

from django.urls import reverse
from product_app.models import Category, Product, SubCategory, Tag
from product_app.tests.utils import (
    get_category,
    get_review,
    get_simple_product,
    get_sub_category,
    get_tag,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class CatalogAPIViewTests(APITestCase):
    """
    Тест CatalogAPIView.
    """

    url = reverse("product_app:catalog")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Подготовка к тестам.

        :return: None.
        """
        super().setUpClass()
        cls.category = get_category()
        cls.sub_category_1 = get_sub_category(cls.category)
        cls.sub_category_2 = get_sub_category(cls.category)

    def setUp(self) -> None:
        """
        Подготовка к каждому тесту.

        :return: None.
        """
        self.list_products_cat_1 = [
            get_simple_product(self.sub_category_1) for _ in range(20)
        ]
        self.list_products_cat_2 = [
            get_simple_product(self.sub_category_2) for _ in range(20)
        ]
        self.valid_data: Dict[str, Any] = dict()
        self.valid_data["filter[name]"] = ""
        self.valid_data["filter[minPrice]"] = 1
        self.valid_data["filter[maxPrice]"] = 10000
        self.valid_data["filter[freeDelivery]"] = False
        self.valid_data["filter[available]"] = True
        self.valid_data["currentPage"] = 1
        self.valid_data["category"] = self.sub_category_1.pk
        self.valid_data["sort"] = "price"
        self.valid_data["sortType"] = "inc"
        self.valid_data["limit"] = 10
        # self.valid_data['tags[]'] пока не включаем, задействуем позже в тестах.

    def test_valid_data(self) -> None:
        """
        Проверяем CatalogAPIView с валидными данными.

        :return: None.
        """
        response: Response = self.client.get(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_count_products_in_page(self) -> None:
        """
        Проверяем CatalogAPIView количество продуктов на страницу.

        :return: None.
        """
        limits_list = [1, 5, 10]
        for limit in limits_list:
            self.valid_data["limit"] = limit
            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["items"]), self.valid_data["limit"])

    def test_sort_price(self) -> None:
        """
        Проверяем сортировку по цене.

        :return: None.
        """
        for i, product in enumerate(self.list_products_cat_1, 1):
            product.price = 100 * i
        Product.objects.bulk_update(self.list_products_cat_1, ["price"])
        sort_types = ["inc", "dec"]
        self.valid_data["sort"] = "price"
        for sort_type in sort_types:
            self.valid_data["sortType"] = sort_type

            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_price = [product["price"] for product in response.data["items"]]
            product_price = [product.price for product in self.list_products_cat_1]

            if sort_type == "dec":
                self.assertEqual(
                    response_price, sorted(product_price)[: self.valid_data["limit"]]
                )
            else:
                self.assertEqual(
                    response_price,
                    sorted(product_price, reverse=True)[: self.valid_data["limit"]],
                )

    def test_sort_date(self) -> None:
        """
        Проверяем сортировку по дате.

        :return: None.
        """
        # Так как у Product поле created_at - это DateTimeField,
        # то проверку можно сделать по времени создания, не изменяя дату.
        sort_types = ["inc", "dec"]
        self.valid_data["sort"] = "date"
        for sort_type in sort_types:
            self.valid_data["sortType"] = sort_type

            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_id = [product["id"] for product in response.data["items"]]

            if sort_type == "dec":
                product_id = [
                    product.pk
                    for product in sorted(
                        self.list_products_cat_1, key=lambda p: p.created_at
                    )
                ]
            else:
                product_id = [
                    product.pk
                    for product in sorted(
                        self.list_products_cat_1,
                        key=lambda p: p.created_at,
                        reverse=True,
                    )
                ]
            self.assertEqual(response_id, product_id[: self.valid_data["limit"]])

    def test_sort_rating(self) -> None:
        """
        Проверяем сортировку по рейтингу.

        :return: None.
        """
        for product in self.list_products_cat_1:
            for _ in range(20):
                get_review(product)

        sort_types = ["inc", "dec"]
        self.valid_data["sort"] = "rating"
        for sort_type in sort_types:
            self.valid_data["sortType"] = sort_type

            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_rating = [product["rating"] for product in response.data["items"]]
            product_rating = [
                product.get_rating() for product in self.list_products_cat_1
            ]
            if sort_type == "dec":
                self.assertEqual(
                    response_rating, sorted(product_rating)[: self.valid_data["limit"]]
                )
            else:
                self.assertEqual(
                    response_rating,
                    sorted(product_rating, reverse=True)[: self.valid_data["limit"]],
                )

    def test_sort_reviews(self) -> None:
        """
        Проверяем сортировку по количеству отзывов.

        :return: None.
        """
        for product in self.list_products_cat_1:
            for _ in range(random.randint(1, 20)):
                get_review(product)

        sort_types = ["inc", "dec"]
        self.valid_data["sort"] = "reviews"
        for sort_type in sort_types:
            self.valid_data["sortType"] = sort_type

            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_reviews = [
                product["reviews"] for product in response.data["items"]
            ]
            product_reviews = [
                product.reviews.count() for product in self.list_products_cat_1
            ]
            if sort_type == "dec":
                self.assertEqual(
                    response_reviews,
                    sorted(product_reviews)[: self.valid_data["limit"]],
                )
            else:
                self.assertEqual(
                    response_reviews,
                    sorted(product_reviews, reverse=True)[: self.valid_data["limit"]],
                )

    def test_get_products_category(self) -> None:
        """
        Проверяем, что продукты показывает той категории, по которой делаем запрос.

        :return: None.
        """

        category_ids = [self.sub_category_1.pk, self.sub_category_2.pk]
        self.valid_data["limit"] = max(
            len(self.list_products_cat_1), len(self.list_products_cat_2)
        )

        for category_id in category_ids:
            self.valid_data["category"] = category_id

            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_id_set = {product["id"] for product in response.data["items"]}
            products = Product.objects.filter(category__pk=category_id)
            product_id_set = {product.pk for product in products}
            self.assertEqual(response_id_set, product_id_set)

    def test_get_products_tags(self) -> None:
        """
        Проверяем выдачу продуктов по выбранным тегам.

        :return: None.
        """
        tags_list = [get_tag() for _ in range(5)]
        for product in self.list_products_cat_1:
            product.tags.add(*random.choices(tags_list, k=random.randint(1, 5)))

        tags_ids_items = (
            [tags_list[0].pk],
            [tags_list[0].pk, tags_list[1].pk],
            [tags_list[2].pk, tags_list[3].pk, tags_list[4].pk],
        )
        self.valid_data["limit"] = max(
            len(self.list_products_cat_1), len(self.list_products_cat_2)
        )
        for tag_items in tags_ids_items:
            self.valid_data["tags[]"] = tag_items

            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            products = Product.objects.prefetch_related("tags").filter(
                tags__id__in=tag_items
            )
            product_id_set = {product.pk for product in products}
            response_id_set = {product["id"] for product in response.data["items"]}
            self.assertEqual(response_id_set, product_id_set)

    def test_filter_name(self) -> None:
        """
        Тестируем фильтр имени.

        :return: None.
        """
        product_1 = self.list_products_cat_1[0]
        product_1.title = "Nokia Lumia 820"
        product_2 = self.list_products_cat_1[1]
        product_2.title = "Nokia 3310"
        Product.objects.bulk_update([product_1, product_2], ["title"])

        names_and_ids = {
            "nokia": {product_1.pk, product_2.pk},
            "lumia": {product_1.pk},
            "nokia 3310": {product_2.pk},
        }
        for name, ids_set in names_and_ids.items():
            self.valid_data["filter[name]"] = name

            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_set_ids = {product["id"] for product in response.data["items"]}
            self.assertEqual(response_set_ids, ids_set)

    def test_filter_min_price(self) -> None:
        """
        Тестируем фильтр минимальной цены.

        :return: None.
        """
        for i, product in enumerate(self.list_products_cat_1, 1):
            product.price = 100 * i
        Product.objects.bulk_update(self.list_products_cat_1, ["price"])
        min_price = random.randint(1, 100 * len(self.list_products_cat_1))
        self.valid_data["filter[minPrice]"] = min_price
        response: Response = self.client.get(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(product["price"] >= min_price for product in response.data["items"])
        )

    def test_filter_max_price(self) -> None:
        """
        Тестируем фильтр максимальной цены.

        :return: None.
        """
        for i, product in enumerate(self.list_products_cat_1, 1):
            product.price = 100 * i
        Product.objects.bulk_update(self.list_products_cat_1, ["price"])
        max_price = random.randint(1, 100 * len(self.list_products_cat_1))
        self.valid_data["filter[maxPrice]"] = max_price
        response: Response = self.client.get(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(product["price"] <= max_price for product in response.data["items"])
        )

    def test_filter_free_delivery(self) -> None:
        """
        Тестируем фильтр бесплатной доставки.

        :return: None
        """
        product_1 = self.list_products_cat_1[0]
        product_1.free_delivery = True
        product_2 = self.list_products_cat_1[1]
        product_2.free_delivery = True
        Product.objects.bulk_update([product_1, product_2], ["free_delivery"])
        free_delivery_ids_set = {product_1.pk, product_2.pk}
        delivery_filters = [True, False]
        self.valid_data["limit"] = max(
            len(self.list_products_cat_1), len(self.list_products_cat_2)
        )
        for delivery_filter in delivery_filters:
            self.valid_data["filter[freeDelivery]"] = delivery_filter
            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_set_ids = {product["id"] for product in response.data["items"]}
            if delivery_filter:
                self.assertEqual(response_set_ids, free_delivery_ids_set)
            else:
                self.assertTrue(free_delivery_ids_set.isdisjoint(response_set_ids))

    def test_filter_available(self) -> None:
        """
        Тестируем фильтр доступности продукта.

        :return: None
        """
        product_1 = self.list_products_cat_1[0]
        product_1.count = 0
        product_2 = self.list_products_cat_1[1]
        product_2.count = 0
        Product.objects.bulk_update([product_1, product_2], ["count"])
        available_ids_set = {product_1.pk, product_2.pk}
        available_filters = [True, False]
        self.valid_data["limit"] = max(
            len(self.list_products_cat_1), len(self.list_products_cat_2)
        )
        for available_filter in available_filters:
            self.valid_data["filter[available]"] = available_filter
            response: Response = self.client.get(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_set_ids = {product["id"] for product in response.data["items"]}
            if not available_filter:
                self.assertEqual(response_set_ids, available_ids_set)
            else:
                self.assertTrue(available_ids_set.isdisjoint(response_set_ids))

    def tearDown(self) -> None:
        """
        Функция удаляет продукты после каждого теста.

        :return: None.
        """
        Product.objects.all().delete()

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
