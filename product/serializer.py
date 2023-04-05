from rest_framework import serializers

from .models import Category, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "description", "rating", "created_at", "updated_at"]

    user = serializers.ReadOnlyField(source="user.username")

    def create(self, validated_data):
        """Overriding to associate review with product"""
        # product_pk is returned from ReviewViewSet
        product_pk = self.context["product_pk"]
        user = self.context["user"]

        return Review.objects.create(
            product_id=product_pk,
            user=user,
            **validated_data,
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "upc",
            "name",
            "image",
            "description",
            "quantity",
            "price",
            "category",
            "created_at",
            "updated_at",
            "reviews",
        ]

    # category = serializers.StringRelatedField()
    reviews = ReviewSerializer(many=True, read_only=True)
    upc = serializers.ReadOnlyField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

    # product = ProductSerializer(many=True, read_only=True)
