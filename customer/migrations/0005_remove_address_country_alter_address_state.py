# Generated by Django 4.1.7 on 2023-03-17 15:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0004_alter_customer_image_alter_membership_discount"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="address",
            name="country",
        ),
        migrations.AlterField(
            model_name="address",
            name="state",
            field=models.CharField(max_length=2),
        ),
    ]
