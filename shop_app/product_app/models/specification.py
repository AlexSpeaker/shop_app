from django.db import models
from django.utils.translation import gettext_lazy as _

from product_app.models.product import Product


class Specification(models.Model):
    """
    Модель спецификации продукта.

    **name** - Название спецификации. \n
    **value** - Значение спецификации. \n
    **product** - Продукт. \n
    """
    name = models.CharField(_("name"), max_length=500, null=False, blank=False)
    value = models.CharField(_("value"), max_length=500, null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )

    def __str__(self) -> str:
        """
        Строковое представление.

        :return: Название.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.

        :return: Specification(Название).
        """
        return f"Specification({self.name})"