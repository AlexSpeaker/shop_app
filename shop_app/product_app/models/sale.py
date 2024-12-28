from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from product_app.models import Product


class Sale(models.Model):
    """
    Модель распродажи.

    **product** - Продукт распродажи. \n
    **date_from** - Начало распродажи. \n
    **date_to** - Конец распродажи. \n
    **price** - Мнимая цена за продукт, якобы цена до распродажи (необязательно должна быть равна настоящей). \n
    **sale_price** - Цена со скидкой. \n
    **created_at** - Дата и время создания акции.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    date_from = models.DateField(_("start date"), null=False, blank=False)
    date_to = models.DateField(_("end date"), null=False, blank=False)
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(Decimal(1))],
    )
    sale_price = models.DecimalField(
        _("sale price"),
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(Decimal(1))],
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def clean(self) -> None:
        """
        Будут проведена валидация данных, ошибки будут отображаться в админ панели.

        :return: None.
        """
        super().clean()
        if not self.date_from:
            raise ValidationError({"date_from": "Это обязательное поле."})
        if not self.date_to:
            raise ValidationError({"date_to": "Это обязательное поле."})
        if not self.price:
            raise ValidationError({"price": "Это обязательное поле."})
        if not self.sale_price:
            raise ValidationError({"sale_price": "Это обязательное поле."})
        if self.date_from >= self.date_to:
            raise ValidationError(
                {"date_to": "Конечная дата должна быть больше стартовой."}
            )
        if self.sale_price >= self.price:
            raise ValidationError(
                {
                    "sale_price": "Цена со скидкой должна быть меньше мнимой цены без скидки."
                }
            )
        if not self.pk:
            sales = Sale.objects.filter(
                Q(date_from__lte=timezone.now().date())
                & Q(date_to__gte=timezone.now().date())
                & Q(product=self.product)
            ).count()
            if sales:
                raise ValidationError(
                    {
                        "date_to": "Распродажа уже идёт, завершите (удалите) старую, что бы начать новую."
                    }
                )

    class Meta:
        verbose_name = _("sale")
        verbose_name_plural = _("sales")
        ordering = ("-date_to",)
