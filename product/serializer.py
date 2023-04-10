from rest_framework import serializers, status

from .models import Category, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "description", "rating", "created_at", "updated_at"]

    user = serializers.ReadOnlyField(source="user.username")

    def validate(self, attrs):
        """Check if user has already reviewed the product"""
        product_pk = self.context["product_pk"]
        user = self.context["user"]

        if Review.objects.filter(user=user, product_id=product_pk).exists():
            raise serializers.ValidationError(
                {"error": "You have already reviewed this product"}
            )
        return attrs

    def create(self, validated_data):
        """Overriding to associate review with product"""
        product_pk = self.context["product_pk"]
        user = self.context["user"]

        return Review.objects.create(
            product_id=product_pk,
            user=user,
            **validated_data,
        )


class ReadProductSerializer(serializers.ModelSerializer):
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
            "average_rating",
            "reviews",
        ]

    reviews = ReviewSerializer(many=True, read_only=True)
    upc = serializers.ReadOnlyField()
    category = serializers.StringRelatedField()


class WriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "image",
            "description",
            "quantity",
            "price",
            "category",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "total_products"]
