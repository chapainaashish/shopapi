from django.contrib import admin

from . import models


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["associated_order", "user", "amount", "status", "updated_at"]
    list_per_page = 10
    readonly_fields = ["order"]
    search_fields = ["order__user__username"]
    list_select_related = ["order", "order__user"]
    list_filter = ["status"]

    def associated_order(self, payment):
        return f"order{str(payment.order.id)}_{str(payment.order.created_at)[:10]}"
