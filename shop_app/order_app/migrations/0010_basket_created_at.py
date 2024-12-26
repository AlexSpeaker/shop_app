# Generated by Django 5.1.4 on 2024-12-26 09:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0009_alter_basket_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="basket",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
