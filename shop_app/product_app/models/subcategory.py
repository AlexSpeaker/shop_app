from django.db import models
from django.utils.translation import gettext_lazy as _
from product_app.models.category import Category


class SubCategory(models.Model):
    """
    Модель подкатегории.

    **name** - Имя подкатегории. \n
    **category** - Категория.
    """

    name = models.CharField(
        _("name"), max_length=100, unique=True, null=False, blank=False
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        """
        Строковое представление.

        :return: Имя.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.

        :return: SubCategory(Имя).
        """
        return f"SubCategory({self.name})"
