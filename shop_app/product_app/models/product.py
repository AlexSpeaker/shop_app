from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from product_app.models.subcategory import SubCategory
from product_app.models.tag import Tag


class Product(models.Model):
    """
    Модель продукта.

    **category** - Категория продукта (является подкатегорией). \n
    **price** - Цена продукта. \n
    **count** - Количество продукта. \n
    **created_at** - Дата создания продукта. \n
    **updated_at** - Дата обновления продукта. \n
    **title** - Название продукта. \n
    **description** - Короткое описание продукта. \n
    **full_description** - Полное описание продукта. \n
    **free_delivery** - Есть ли бесплатная доставка. \n
    **tags** - Теги продукта.  \n
    **archived** - Является ли продукт архивированным.
    """

    category = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, related_name="products"
    )
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
    )

    count = models.IntegerField(
        _("count"),
        default=0,
        null=False,
        blank=False,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(
        _("created at"), auto_now_add=True, null=False, blank=False
    )
    updated_at = models.DateTimeField(
        _("updated at"), auto_now=True, null=False, blank=False
    )
    title = models.CharField(_("title"), max_length=500, null=False, blank=False)
    description = models.TextField(_("description"), null=False, blank=False)
    full_description = models.TextField(_("full description"), null=False, blank=False)
    free_delivery = models.BooleanField(
        _("free delivery"), default=False, null=False, blank=False
    )
    tags = models.ManyToManyField(Tag, verbose_name=_("tags"), related_name="products")
    archived = models.BooleanField(
        _("archived"), default=False, null=False, blank=False
    )

    def __str__(self) -> str:
        """
        Строковое представление.

        :return: Название.
        """
        return self.title

    def __repr__(self) -> str:
        """
        Строковое представление для отладки.

        :return: Product(Название).
        """
        return f"Product({self.title})"
