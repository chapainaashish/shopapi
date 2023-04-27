from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "delivery",
        "total_price",
        "shipping_address_link",
        "billing_address_link",
        "created_at",
    ]

    search_fields = ["user__username"]
    list_select_related = ["user"]
    list_filter = ["delivery"]

    def shipping_address_link(self, obj):
        url = reverse("admin:user_address_change", args=[obj.shipping_address.pk])
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.shipping_address))

    def billing_address_link(self, obj):
        url = reverse("admin:user_address_change", args=[obj.billing_address.pk])
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.billing_address))

    billing_address_link.short_description = "Billing Address"
    shipping_address_link.short_description = "Shipping Address"


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "order_link",
        "product_link",
        "ordered_price",
        "quantity",
        "total_price",
    ]
    search_fields = ["product__name"]
    list_select_related = ["order", "product"]

    def order_link(self, obj):
        url = reverse("admin:order_order_change", args=[obj.order.pk])
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.order))

    def product_link(self, obj):
        url = reverse("admin:product_product_change", args=[obj.product.pk])
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.product))

    order_link.short_description = "Associated Order"
    product_link.short_description = "Product"
