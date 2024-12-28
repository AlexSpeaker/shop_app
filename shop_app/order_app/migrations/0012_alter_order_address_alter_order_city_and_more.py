# Generated by Django 5.1.4 on 2024-12-27 08:35

from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0011_basket_fixed_price_order_basket_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.CharField(
                default=None, max_length=255, null=True, verbose_name="address"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="city",
            field=models.CharField(
                default=None, max_length=16, null=True, verbose_name="city"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="delivery_type",
            field=models.CharField(
                default=None, max_length=16, null=True, verbose_name="delivery type"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="email",
            field=models.EmailField(
                default=None, max_length=254, null=True, verbose_name="email"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_type",
            field=models.CharField(
                default=None, max_length=16, null=True, verbose_name="payment type"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="phone",
            field=models.CharField(
                default=None, max_length=17, null=True, verbose_name="phone"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                default=None, max_length=16, null=True, verbose_name="status"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_cost",
            field=models.DecimalField(
                decimal_places=2,
                default=None,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
    ]