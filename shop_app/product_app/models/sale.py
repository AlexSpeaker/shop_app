from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from product_app.models import Product


class Sale(models.Model):
    """
    Модель распродажи.

    **product** - Продукт распродажи. \n
    **date_from** - Начало распродажи. \n
    **date_to** - Конец распродажи. \n
    **price** - Мнимая цена за продукт, якобы цена до распродажи (необязательно должна быть равна настоящей). \n
    **sale_price** - Цена со скидкой.
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
        validators=[MinValueValidator(1)],
    )
    sale_price = models.DecimalField(
        _("sale price"),
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
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

    class Meta:
        verbose_name = _("sale")
        verbose_name_plural = _("sales")
        ordering = ("-created_at",)
