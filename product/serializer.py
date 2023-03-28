from rest_framework import serializers

from .models import Category, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "rating", "review"]

    user = serializers.ReadOnlyField(source="user.username")

    def create(self, validated_data):
        product_id = self.context["product_id"]
        user = self.context["user"]

        return Review.objects.create(
            product_id=product_id,
            user=user,
            **validated_data,
        )


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
            "reviews",
        ]

    category = serializers.StringRelatedField()
    reviews = ReviewSerializer(many=True, read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

    # product = ProductSerializer(many=True, read_only=True)
