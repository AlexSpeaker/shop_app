from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from product_app.models import Product


class Basket(models.Model):
    """
    Модель корзины покупок.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="baskets"
    )
    count = models.IntegerField(
        _("count"), validators=[MinValueValidator(1)], null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baskets")
