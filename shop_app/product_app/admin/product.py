from datetime import date
from typing import TYPE_CHECKING, Any, Optional

from django.contrib import admin
from django.db.models import QuerySet
from django.forms import BaseInlineFormSet as _BaseInlineFormSet
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString
from django.utils.translation import gettext_lazy as _
from product_app.models import Product, ProductImage, Review, Sale, Specification

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[Product]
    ImageTabularInline = admin.TabularInline[ProductImage, Product]
    ReviewTabularInline = admin.TabularInline[Review, Product]
    SaleTabularInline = admin.TabularInline[Sale, Product]
    SpecificationTabularInline = admin.TabularInline[Specification, Product]
    BaseInlineFormSet = _BaseInlineFormSet[Sale, Product, ModelForm[Sale]]
else:

    ModelAdmin = admin.ModelAdmin
    ImageTabularInline = admin.TabularInline
    ReviewTabularInline = admin.TabularInline
    SaleTabularInline = admin.TabularInline
    SpecificationTabularInline = admin.TabularInline
    BaseInlineFormSet = _BaseInlineFormSet


class CustomInlineFormSet(BaseInlineFormSet):
    """
    Переопределяем класс BaseInlineFormSet.
    """

    forms: Any
    obj: Optional[Product] = None

    def __init__(self, *args_c: Any, **kwargs_c: Any):
        """
        Добавим в известные поля (ещё не созданной сущности) значения по умолчанию.
        Price - будет браться из рассматриваемого продукта.
        Date_from - текущая дата.

        :param args_c: Any.
        :param kwargs_c: Any.
        """
        super().__init__(*args_c, **kwargs_c)
        if self.obj:
            for _form in self.forms:
                if not _form.instance.pk:
                    _form.initial["price"] = self.obj.price
                    _form.initial["date_from"] = date.today()


class ProductImageInline(ImageTabularInline):
    """
    Inline класс изображений продукта.
    """

    model = ProductImage
    verbose_name_plural = _("Images")
    extra = 1


class ProductReviewsInline(ReviewTabularInline):
    """
    Inline класс отзывов на продукт.
    """

    model = Review
    verbose_name_plural = _("Reviews")
    extra = 0
    classes = ("collapse",)


class ProductSaleInline(SaleTabularInline):
    """
    Inline класс распродаж на продукт.
    """

    model = Sale
    verbose_name_plural = _("Sales")
    extra = 1
    formset = CustomInlineFormSet
    fields = ("created_at", "date_from", "date_to", "price", "sale_price", "relevant")
    readonly_fields = ("created_at", "relevant")

    @staticmethod
    def relevant(obj: Sale) -> SafeString:
        """
        Функция покажет актуальна ли акция на данный момент.

        :param obj: Sale.
        :return: False, если не актуальна, иначе True (их представления в виде изображения).
            Если объект ещё не создан, то вернёт 'Not defined'.
        """
        if obj.pk and obj.date_to and obj.date_to >= date.today():
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="Yes" />')
        elif obj.pk and obj.date_to and obj.date_to < date.today():
            return format_html('<img src="/static/admin/img/icon-no.svg" alt="No" />')
        return format_html(f'<p>{_("Not defined")}</p>')

    def get_formset(
        self, request: HttpRequest, obj: Optional[Product] = None, **kwargs: Any
    ) -> Any:
        """
        Переопределяем стандартный formset,
        чтобы подставлять значения по умолчанию ещё не созданным сущностям.

        :param request: HttpRequest.
        :param obj: Optional[Product].
        :param kwargs: Any.
        :return: Any.
        """
        formset = super().get_formset(request, obj, **kwargs)
        formset.obj = obj
        return formset


class ProductSpecificationInline(SpecificationTabularInline):
    """
    Inline класс спецификаций продукта.
    """

    model = Specification
    verbose_name_plural = _("Specifications")
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Класс админка для продукта.
    """

    inlines = (
        ProductImageInline,
        ProductReviewsInline,
        ProductSaleInline,
        ProductSpecificationInline,
    )
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
