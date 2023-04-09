from rest_framework import serializers

from .models import Address, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "image", "phone"]

    def create(self, validated_data):
        return Profile.objects.create(user=self.context.get("user"), **validated_data)

    user = serializers.StringRelatedField(read_only=True)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "user", "house_no", "street", "city", "postal_code", "country"]

    user = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        return Address.objects.create(user=self.context.get("user"), **validated_data)
