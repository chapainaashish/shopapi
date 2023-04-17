from rest_framework import serializers

from .models import Category, Product, ProductImage, Review


class ReadReviewSerializer(serializers.ModelSerializer):
    """Serializer class of Review model for reading review [GET]"""

    class Meta:
        model = Review
        fields = ["id", "user", "description", "rating", "created_at", "updated_at"]

    user = serializers.ReadOnlyField(source="user.username")


class WriteReviewSerializer(serializers.ModelSerializer):
    """Serializer class of Review model for writing review [POST, PATCH]"""

    class Meta:
        model = Review
        fields = ["id", "description", "rating"]

    id = serializers.ReadOnlyField()

    def validate(self, attrs):
        """Overriding to check if the product exists and  user has already reviewed the product or not"""

        product_pk = self.context["product_pk"]
        user = self.context["user"]

        # checking if request have valid product_pk and product exist
        product = Product.objects.filter(pk=product_pk)
        if not product.exists():
            raise serializers.ValidationError({"error": "Product doesn't exist"})

        # checking if user has already reviewed the product or not
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


class ReadProductSerializer(serializers.ModelSerializer):
    """Serializer class of Product model for reading product [GET]"""

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

    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReadReviewSerializer(many=True, read_only=True)


class WriteProductSerializer(serializers.ModelSerializer):
    """Serializer class of Product model for writing product [POST, PUT, PATCH]"""

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "quantity",
            "price",
            "category",
        ]

        id = serializers.ReadOnlyField()


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
