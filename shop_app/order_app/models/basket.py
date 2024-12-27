from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from order_app.models.order import Order
from product_app.models import Product


class Basket(models.Model):
    """
    Модель корзины покупок.

    **product** Связанный продукт. \n
    **count** Необходимое количество продукта. \n
    **user** Связанный пользователь,
        если он прошёл аутентификацию. \n
    **session_id** Связанный анонимный пользователь,
        если пользователь не прошёл аутентификацию.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="baskets"
    )
    count = models.IntegerField(
        _("count"),
        validators=[MinValueValidator(1)],
        null=False,
        blank=False,
        default=0,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="baskets", null=True, default=None
    )
    session_id = models.CharField(null=True, default=None)
    created_at = models.DateField(auto_now_add=True)
    fixed_price = models.DecimalField(
        default=None,
        null=True,
        blank=False,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="baskets", null=True, default=None
    )
