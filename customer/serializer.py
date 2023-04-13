from rest_framework import serializers

from .models import Address, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer of Profile model [*]"""

    class Meta:
        model = Profile
        fields = ["id", "image", "phone"]

    def validate(self, attrs):
        """Override to validate one user can have only one profile"""
        if Profile.objects.filter(user=self.context["user"]).exists():
            raise serializers.ValidationError({"error": "You already have a profile"})
        return attrs

    def create(self, validated_data):
        """Creating profile object of associated user"""
        return Profile.objects.create(user=self.context.get("user"), **validated_data)


class ReadAddressSerializer(serializers.ModelSerializer):
    """Serializer of Address model for reading[GET]"""

    class Meta:
        model = Address
        fields = ["id", "house_no", "street", "city", "postal_code", "country"]


class WriteAddressSerializer(serializers.ModelSerializer):
    """Serializer of Address model for writing [POST, PUT, PATCH]"""

    class Meta:
        model = Address
        fields = ["house_no", "street", "city", "postal_code", "country"]

    def create(self, validated_data):
        """Creating address object of associated user"""
        return Address.objects.create(user=self.context.get("user"), **validated_data)
