from rest_framework import serializers

from .models import Category, Product, ProductImage, Review


class ReadReviewSerializer(serializers.ModelSerializer):
    """Serializer class of Review model for reading [GET]"""

    class Meta:
        model = Review
        fields = ["id", "user", "description", "rating", "created_at", "updated_at"]

    user = serializers.ReadOnlyField(source="user.username")


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer class of ProductImage model [*]"""

    class Meta:
        model = ProductImage
        fields = ["id", "image"]

    id = serializers.ReadOnlyField()

    def create(self, validated_data):
        """Overriding to associate image with related product"""
        return ProductImage.objects.create(
            product_id=self.context["product_pk"], **validated_data
        )


class WriteReviewSerializer(serializers.ModelSerializer):
    """Serializer class of Review model for writing [POST, PATCH]"""

    class Meta:
        model = Review
        fields = ["description", "rating"]

    def validate(self, attrs):
        """Overriding to check if user has already reviewed the product or not"""
        product_pk = self.context["product_pk"]
        user = self.context["user"]
        review_exists = Review.objects.filter(user=user, product_id=product_pk).exists()

        if self.context["request"].method == "POST" and review_exists:
            raise serializers.ValidationError(
                {"error": "You have already reviewed this product"}
            )

        return attrs

    def create(self, validated_data):
        """Overriding to associate review with related product"""
        product_pk = self.context["product_pk"]
        user = self.context["user"]

        return Review.objects.create(
            product_id=product_pk,
            user=user,
            **validated_data,
        )


class ReadProductSerializer(serializers.ModelSerializer):
    """Serializer class of Product model for reading [GET]"""

    class Meta:
        model = Product
        fields = [
            "id",
            "upc",
            "name",
            "description",
            "quantity",
            "price",
            "category",
            "created_at",
            "updated_at",
            "average_rating",
            "images",
            "reviews",
        ]

    # for nested relationship
    reviews = ReadReviewSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)


class WriteProductSerializer(serializers.ModelSerializer):
    """Serializer class of Product model for writing [POST, PUT, PATCH]"""

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "quantity",
            "price",
            "category",
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Serializer class of Category model [*]"""

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "total_products",
            "created_at",
            "updated_at",
        ]
