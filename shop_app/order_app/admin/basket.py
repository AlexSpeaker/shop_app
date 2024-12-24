from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from order_app.models import Basket

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[Basket]
else:

    ModelAdmin = admin.ModelAdmin


@admin.register(Basket)
class BasketAdmin(ModelAdmin):
    """
    Класс админка для корзины продуктов.
    """

    list_display = ("pk", "product_name", "count")
    list_display_links = (
        "pk",
        "product_name",
    )
    search_fields = ("name",)

    @staticmethod
    def product_name(obj: Basket) -> Any:
        """
        Получение имени продукта.

        :param obj: Basket
        :return: Имя продукта.
        """
        return obj.product.title

    def get_queryset(self, request: HttpRequest) -> QuerySet[Basket, Basket]:
        """
        Подцепим подкатегории.

        :param request: HttpRequest.
        :return: QuerySet[Category, Category].
        """
        return super().get_queryset(request).prefetch_related("product")
