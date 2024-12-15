from datetime import date
from typing import TYPE_CHECKING, Any, Optional

from django.contrib import admin
from django.db.models import QuerySet
from django.forms import BaseInlineFormSet as _BaseInlineFormSet
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from product_app.models import Product, ProductImage, Review, Sale

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[Product]
    ImageTabularInline = admin.TabularInline[ProductImage, Product]
    ReviewTabularInline = admin.TabularInline[Review, Product]
    SaleTabularInline = admin.TabularInline[Sale, Product]
    BaseInlineFormSet = _BaseInlineFormSet[Sale, Product, ModelForm[Sale]]
else:

    ModelAdmin = admin.ModelAdmin
    ImageTabularInline = admin.TabularInline
    ReviewTabularInline = admin.TabularInline
    SaleTabularInline = admin.TabularInline
    BaseInlineFormSet = _BaseInlineFormSet


class CustomInlineFormSet(BaseInlineFormSet):
    forms: Any
    obj: Optional[Product] = None

    def __init__(self, *args_c: Any, **kwargs_c: Any):
        super().__init__(*args_c, **kwargs_c)
        if self.obj:
            for _form in self.forms:
                if not _form.instance.pk:
                    _form.initial["price"] = self.obj.price
                    _form.initial["date_from"] = date.today()



class ProductImageInline(ImageTabularInline):
    model = ProductImage
    verbose_name_plural = _("Images")
    extra = 1


class ProductReviewsInline(ReviewTabularInline):
    model = Review
    verbose_name_plural = _("Reviews")
    extra = 0
    classes = ("collapse",)


class ProductSaleInline(SaleTabularInline):
    model = Sale
    verbose_name_plural = _("Sales")
    extra = 1
    formset = CustomInlineFormSet

    def get_formset(
        self, request: HttpRequest, obj: Optional[Product] = None, **kwargs: Any
    ) -> Any:
        formset = super().get_formset(request, obj, **kwargs)
        formset.obj = obj
        return formset


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Класс админка для продукта.
    """

    inlines = (ProductImageInline, ProductReviewsInline, ProductSaleInline)
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
            .prefetch_related("tags", "images", "reviews", "sales")
        )
