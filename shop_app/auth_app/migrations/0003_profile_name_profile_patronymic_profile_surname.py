# Generated by Django 5.1.4 on 2024-12-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0002_alter_profile_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="name",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AddField(
            model_name="profile",
            name="patronymic",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AddField(
            model_name="profile",
            name="surname",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
    ]