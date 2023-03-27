from rest_framework import serializers

from .models import Category, Product, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "image", "description", "quantity", "price", "category"]

    # category = serializers.StringRelatedField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

    # product = ProductSerializer()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["user", "product", "rating", "review"]

    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
