from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Модель категории.

    **name** - Имя категории.
    """

    name = models.CharField(
        _("name"), max_length=100, unique=True, null=False, blank=False
    )

    def __str__(self) -> str:
        """
        Строковое представление.

        :return: Имя.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.

        :return: Category(Имя).
        """
        return f"Category({self.name})"
