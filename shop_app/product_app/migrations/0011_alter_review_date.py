# Generated by Django 5.1.4 on 2024-12-21 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0010_alter_product_full_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="created at"),
        ),
    ]
