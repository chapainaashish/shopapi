from rest_framework import serializers

from .models import Address, Customer, Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["membership", "discount"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "image", "email", "phone", "membership"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["customer", "house_no", "street", "city", "state", "country"]
