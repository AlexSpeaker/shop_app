# Generated by Django 5.1.4 on 2024-12-18 14:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0002_remove_review_user_review_author_alter_review_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="email",
            field=models.EmailField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]