from datetime import date
from decimal import Decimal
from typing import Optional, List

from django.db.models import Avg, Q
from django.db.models.fields.files import ImageFieldFile
from product_app.models import Product, ProductImage, Review, Sale, Specification
from product_app.serializers.review import ReviewSerializer
from product_app.serializers.tag import OutTagSerializer
from rest_framework import serializers


class OutProductImageSerializer(serializers.ModelSerializer[ProductImage]):
    src = serializers.SerializerMethodField(read_only=True)
    alt = serializers.CharField(read_only=True, source="title")

    class Meta:
        model = ProductImage
        fields = ("src", "alt")

    @staticmethod
    def get_src(obj: ProductImage) -> Optional[str]:
        """
        Функция проверит image. Если существует, то вернёт его url, иначе None.

        :param obj: ProductImage.
        :return: Если существует image, то вернёт его url, иначе None.
        """
        if obj.image:
            return obj.image.url
        return None


class OutSpecificationSerializer(serializers.ModelSerializer[Specification]):

    class Meta:
        model = Specification
        fields = "name", "value"


class OutProductSerializer(serializers.ModelSerializer[Product]):
    """
    Serializer для модели Product.
    """

    id = serializers.IntegerField(read_only=True, source="pk")
    category = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateTimeField(read_only=True, source="created_at")
    fullDescription = serializers.CharField(read_only=True, source="full_description")
    freeDelivery = serializers.BooleanField(read_only=True, source="free_delivery")
    tags = serializers.SerializerMethodField(read_only=True)
    images = OutProductImageSerializer(many=True, read_only=True)
    specifications = OutSpecificationSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "tags",
            "images",
            "specifications",
            "rating",
            "reviews",
        )

    @staticmethod
    def get_price(obj: Product) -> Decimal:
        """
        Определит текущую цену на продукт (учитывает действующую акцию).

        :param obj: Product.
        :return: Цена.
        """

        sale = Sale.objects.filter(Q(product=obj), Q(date_to__gte=date.today())).first()
        return sale.sale_price if sale else obj.price

    @staticmethod
    def get_rating(obj: Product) -> Optional[float]:
        """
        Функция определит средний рейтинг продукта.
        Если рейтинга ещё нет - вернёт None.

        :param obj: Product.
        :return: Optional[float].
        """

        rating = Review.objects.filter(product=obj).aggregate(rating=Avg("rate"))
        return round(rating["rating"], 2) if rating else None

    @staticmethod
    def get_category(obj: Product) -> int:
        """
        Возвращает id подкатегории, к которой принадлежит продукт.

        :param obj: Product.
        :return: Id подкатегории.
        """
        return int(obj.category.pk)

    @staticmethod
    def get_tags(obj: Product) -> List[str]:
        return [tag.name for tag in obj.tags.all()]