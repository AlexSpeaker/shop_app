# Generated by Django 5.1.4 on 2024-12-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0013_remove_order_total_cost"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="paid_for",
            field=models.BooleanField(default=False, verbose_name="paid for"),
        ),
    ]
