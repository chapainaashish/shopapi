# Generated by Django 4.1.7 on 2023-04-17 14:53

from django.db import migrations, models
import django.utils.timezone
import product.models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ("-created_at",), "verbose_name_plural": "Categories"},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AlterModelOptions(
            name="productimage",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AlterModelOptions(
            name="review",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddField(
            model_name="productimage",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Enter the product image",
                upload_to=product.models.product_image_path,
            ),
        ),
    ]