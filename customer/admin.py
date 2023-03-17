from django.contrib import admin

from .models import Address, Customer, Membership

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Membership)
