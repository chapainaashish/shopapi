# Generated by Django 4.1.7 on 2023-04-17 14:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cart",
            options={"ordering": ("-created_at",)},
        ),
    ]