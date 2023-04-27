from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "image", "phone", "updated_at"]
    search_fields = ["user__username"]


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "house_no", "city", "country", "updated_at"]
    search_fields = ["user__username"]
    list_select_related = ["user"]
    list_filter = ["country"]
