from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import models


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "updated_at"]
    search_fields = ["user__username"]


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        "cart",
        "product_link",
        "quantity",
        "unit_price",
        "total_price",
    ]
    search_fields = ["product__name"]
    list_select_related = ["cart", "product"]

    def product_link(self, obj):
        url = reverse("admin:product_product_change", args=[obj.product.pk])
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.product))

    product_link.short_description = "Product"
