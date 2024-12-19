from decimal import Decimal
from typing import Optional

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone
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

    def get_actual_price(self) -> Decimal:
        """
        Возвращает цену с учетом активной акции.
        :return: Актуальная цена.
        """
        today = timezone.now().date()
        active_sale = self.sales.filter(
            date_from__lte=today, date_to__gte=today
        ).first()
        return active_sale.sale_price if active_sale else self.price

    def get_imaginary_price(self) -> Optional[Decimal]:
        """
        Возвращает мнимую цену с учетом активной акции.
        Эта та цена, которая якобы была до акции (задаётся при создании акции).

        :return: Мнимую цену, если акция есть, иначе None.
        """
        today = timezone.now().date()
        active_sale = self.sales.filter(
            date_from__lte=today, date_to__gte=today
        ).first()
        return active_sale.price if active_sale else None

    def get_rating(self) -> Optional[float]:
        """
        Вернёт средний рейтинг продукта.

        :return: Средний рейтинг.
        """
        rating = self.reviews.aggregate(rating=Avg("rate"))
        return round(rating["rating"], 2) if rating["rating"] else None

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
