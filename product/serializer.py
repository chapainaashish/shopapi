from rest_framework import serializers

from .models import Category, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "rating", "review"]

    user = serializers.ReadOnlyField(source="user.username")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "description",
            "quantity",
            "price",
            "category",
            "review",
        ]

    category = serializers.StringRelatedField()
    review = ReviewSerializer(many=True, read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
