# Generated by Django 5.1.4 on 2024-12-27 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0014_order_paid_for"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="status",
        ),
    ]
