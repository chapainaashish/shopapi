# Generated by Django 4.1.7 on 2023-04-27 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Enter your image",
                        null=True,
                        upload_to="user/images",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        help_text="Enter your phone number", max_length=128, region=None
                    ),
                ),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "house_no",
                    models.CharField(help_text="Enter the house no", max_length=255),
                ),
                (
                    "street",
                    models.CharField(help_text="Enter the street", max_length=255),
                ),
                ("city", models.CharField(help_text="Enter the city", max_length=255)),
                (
                    "postal_code",
                    models.CharField(help_text="Enter the postal code", max_length=20),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        help_text="Enter the country", max_length=2
                    ),
                ),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
