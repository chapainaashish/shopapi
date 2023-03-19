from rest_framework import serializers

from .models import Address, Profile

# class MembershipSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Membership
#         fields = ["membership", "discount"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "image", "email", "phone"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["Profile", "house_no", "street", "city", "state", "country"]
