from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "total_products", "updated_at"]
    list_per_page = 10
    search_fields = ["name", "description"]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "category",
        "quantity",
        "average_rating",
        "updated_at",
    ]
    list_per_page = 10
    list_select_related = ["category"]
    readonly_fields = ["upc"]
    search_fields = ["name", "description"]
    list_filter = ["category"]


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image", "created_at"]
    list_per_page = 10
    list_select_related = ["product"]
    search_fields = ["product"]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating", "updated_at"]
    list_per_page = 10
    search_fields = ["product"]
    list_filter = ["rating"]
