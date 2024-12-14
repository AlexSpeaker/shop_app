from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    """
    Модель тега.

    **name** - Имя тега.
    """

    name = models.CharField(_("name"), max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        """
        Строковое представление.

        :return: Имя.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.

        :return: Tag(Имя).
        """
        return f"Tag({self.name})"
