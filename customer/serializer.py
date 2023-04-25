from rest_framework import serializers

from .models import Address, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer class of User Profile model [*]"""

    class Meta:
        model = Profile
        fields = ["id", "image", "phone", "updated_at"]

    def validate(self, attrs):
        """Overriding to validate one user can have only one profile"""
        profile_exists = Profile.objects.filter(user=self.context["user"]).exists()

        if profile_exists and self.context["request_method"] == "POST":
            raise serializers.ValidationError({"error": "You already have a profile"})

        return attrs

    def create(self, validated_data):
        """Creating the user profile of requested user"""
        return Profile.objects.create(user=self.context.get("user"), **validated_data)


class ReadAddressSerializer(serializers.ModelSerializer):
    """Serializer of Address model for reading user address [GET]"""

    class Meta:
        model = Address
        fields = ["id", "house_no", "street", "city", "postal_code", "country"]


class WriteAddressSerializer(serializers.ModelSerializer):
    """Serializer of Address model for writing user address [POST, PUT, PATCH]"""

    class Meta:
        model = Address
        fields = ["house_no", "street", "city", "postal_code", "country"]

    def create(self, validated_data):
        """Creating an address of requested user"""
        return Address.objects.create(user=self.context.get("user"), **validated_data)
