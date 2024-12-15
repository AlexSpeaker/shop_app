from typing import TYPE_CHECKING

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from product_app.models import Product, ProductImage, Review

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[Product]
    ImageTabularInline = admin.TabularInline[ProductImage, Product]
    ReviewTabularInline = admin.TabularInline[Review, Product]
else:

    ModelAdmin = admin.ModelAdmin
    ImageTabularInline = admin.TabularInline
    ReviewTabularInline = admin.TabularInline


class ProductImageInline(ImageTabularInline):
    model = ProductImage
    verbose_name_plural = _("Images")
    extra = 1


class ProductReviewsInline(ReviewTabularInline):
    model = Review
    verbose_name_plural = _("Reviews")
    extra = 0
    classes = ("collapse",)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Класс админка для продукта.
    """

    inlines = (ProductImageInline, ProductReviewsInline)
    list_display = ("pk", "title", "price", "count", "archived")
    list_display_links = (
        "pk",
        "title",
    )
    search_fields = ("title",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Product, Product]:
        """
        Подцепим к продуктам связанные сущности.

        :param request: HttpRequest.
        :return: QuerySet[Product, Product].
        """
        return (
            super()
            .get_queryset(request)
            .select_related("category")
            .prefetch_related("tags", "images", "reviews")
        )
