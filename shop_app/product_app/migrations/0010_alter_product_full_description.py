# Generated by Django 5.1.4 on 2024-12-18 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0009_rename_created_at_review_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="full_description",
            field=models.TextField(verbose_name="full description"),
        ),
    ]
