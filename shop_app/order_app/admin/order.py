from typing import TYPE_CHECKING, Any, Dict
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest

from order_app.models import Basket
from order_app.models.order import Order
from product_app.models import Product

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[Order]
    TabularInline = admin.TabularInline[Basket, Order]
else:

    ModelAdmin = admin.ModelAdmin
    TabularInline = admin.TabularInline

class BasketInline(TabularInline):
    """
    Инлайн класс для корзины.
    """

    model = Basket
    can_delete = False
    verbose_name_plural = _("Baskets")
    extra = 0
    max_num = 0
    fields = ['product', 'count', 'user', 'session_id', 'fixed_price']
    readonly_fields = fields

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """
    Класс админка для заказов.
    """
    inlines = [BasketInline]

    list_display = "created_at", "paid_for"
    list_display_links = ["created_at"]
    readonly_fields = (
        "created_at",
        "user",
        "session_id",
        "full_name",
        "email",
        "phone",
        "delivery_type",
        "payment_type",
        "status",
        "city",
        "address",
        "paid_for",
    )

    @staticmethod
    def has_add_permission(*args: Any, **kwargs: Any) -> bool:
        """
        Запрещаем создавать новые сущности.

        :param args: Any.
        :param kwargs: Any.
        :return: bool.
        """

        return False

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[Order]:
        """
        Получение queryset.

        :param args: Any.
        :param kwargs: Any.
        :return: QuerySet[Order].
        """
        return (
            super()
            .get_queryset(*args, **kwargs)
            .select_related("user")
            .prefetch_related(
                "baskets",
                "baskets__product",
                "baskets__product__category",
                "baskets__user",
                "baskets__product__tags",
                "baskets__product__images",
                "baskets__product__reviews",
                "baskets__product__sales",
            )
        )

    def delete_model(self, request: HttpRequest, obj: Order) -> None:
        """
        Если заказ не завершён, возвращаем продуктам единицы.

        :param request: HttpRequest.
        :param obj: Order.
        :return: None.
        """
        with transaction.atomic():
            if not obj.paid_for:
                products: Dict[str, Product] = dict()
                for basket in obj.baskets.all():
                    product = products.setdefault(str(basket.product.pk), basket.product)
                    product.count += basket.count
                Product.objects.bulk_update(products.values(), ["count"])
            super().delete_model(request, obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Order]) -> None:
        """
        Если какой-нибудь заказ не завершён, возвращаем продуктам единицы.
        :param request: HttpRequest.
        :param queryset: QuerySet[Order].
        :return: None
        """
        with transaction.atomic():
            products: Dict[str, Product] = dict()
            for order in queryset:
                if not order.paid_for:
                    for basket in order.baskets.all():
                        product = products.setdefault(str(basket.product.pk), basket.product)
                        product.count += basket.count
            if products:
                Product.objects.bulk_update(products.values(), ["count"])
            super().delete_queryset(request, queryset)

    @staticmethod
    def has_change_permission(*args: Any, **kwargs: Any) -> bool:
        """
        Запрещаем редактирование.

        :param args: Any.
        :param kwargs: Any.
        :return: bool.
        """
        return False