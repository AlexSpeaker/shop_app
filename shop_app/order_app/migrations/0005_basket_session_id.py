# Generated by Django 5.1.4 on 2024-12-25 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0004_remove_basket_session_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="basket",
            name="session_id",
            field=models.IntegerField(default=None, null=True),
        ),
    ]
