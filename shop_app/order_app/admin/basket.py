from typing import TYPE_CHECKING, Any, Dict

from django.contrib import admin, messages
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest
from order_app.models import Basket
from product_app.models import Product

if TYPE_CHECKING:

    ModelAdmin = admin.ModelAdmin[Basket]
else:

    ModelAdmin = admin.ModelAdmin


@admin.register(Basket)
class BasketAdmin(ModelAdmin):
    """
    Класс админка для корзины продуктов.
    """

    list_display = ("pk", "product_name", "count", "order", "created_at")
    list_display_links = (
        "pk",
        "product_name",
    )
    readonly_fields = ("count", "product", "order", "fixed_price", "session_id", "user")

    @staticmethod
    def product_name(obj: Basket) -> Any:
        """
        Получение имени продукта.

        :param obj: Basket
        :return: Имя продукта.
        """
        return obj.product.title

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[Basket]:
        """
        Получение queryset.

        :param args: Any.
        :param kwargs: Any.
        :return: QuerySet[Basket].
        """
        return (
            super()
            .get_queryset(*args, **kwargs)
            .select_related("order")
            .prefetch_related("product")
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

    def delete_model(self, request: HttpRequest, obj: Basket) -> None:
        """
        Перед удалением проверяем, есть ли привязанный заказ.
        Если есть - запрещаем, если нет удаляем и возвращаем продукту единицы.

        :param request: HttpRequest.
        :param obj: Basket.
        :return: None.
        """
        if obj.order:
            messages.set_level(request, messages.ERROR)
            message = (
                f"Корзина с id={obj.pk} привязана к заказу с id={obj.order.pk}. "
                f"Нельзя удалять корзину привязанную к заказу."
            )
            self.message_user(request, message, level=messages.ERROR)
        else:
            with transaction.atomic():
                product = obj.product
                product.count += obj.count
                product.save()
                obj.delete()

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Basket]) -> None:
        """
        Перед удалением проверяем, есть ли привязанный заказ.
        Если есть - запрещаем, если нет удаляем и возвращаем продукту единицы.

        :param request:
        :param queryset:
        :return:
        """
        if all(basket.order is None for basket in queryset):
            with transaction.atomic():
                products: Dict[str, Product] = dict()
                for basket in queryset:
                    product = products.setdefault(
                        str(basket.product.pk), basket.product
                    )
                    product.count += basket.count
                Product.objects.bulk_update(products.values(), ["count"])
                queryset.delete()
        else:
            messages.set_level(request, messages.ERROR)
            message = "Одна или более корзин привязана к заказу. Удаление запрещено."
            self.message_user(request, message, level=messages.ERROR)

    @staticmethod
    def has_change_permission(*args: Any, **kwargs: Any) -> bool:
        """
        Запрещаем редактирование.

        :param args: Any.
        :param kwargs: Any.
        :return: bool.
        """
        return False
