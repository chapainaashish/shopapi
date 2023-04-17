from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer class of CartItem model [GET, POST, DELETE]"""

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "unit_price", "total_price"]

    def create(self, validated_data):
        """Add product item to the cart, if it is already increase the quantity"""

        cart_pk = self.context["cart_pk"]
        product = validated_data["product"]

        cart_item, created = CartItem.objects.get_or_create(
            product__id=product.id, cart_id=cart_pk, defaults=validated_data
        )

        # increasing the item quantity only if product isn't in the cart
        if not created:
            cart_item.quantity += validated_data["quantity"]
            cart_item.save()

        return cart_item

    def validate(self, data):
        """Overriding to validate cart item quantity isn't greater than actual product quantity"""

        # checking if request have valid cart_pk and cart exist
        cart = Cart.objects.filter(
            pk=self.context["cart_pk"], user=self.context["user"]
        )

        if not cart.exists():
            raise serializers.ValidationError({"error": "Cart doesn't exist"})

        product = data["product"]
        try:
            cart_item = CartItem.objects.get(
                product=product, cart_id=self.context["cart_pk"]
            )
            quantity = cart_item.quantity
        except CartItem.DoesNotExist:
            quantity = 0

        total_quantity = data["quantity"] + quantity
        if total_quantity > product.quantity:
            raise serializers.ValidationError({"error": "Product quantity exceeded"})
        return data


class UpdateCartItemSerializer(serializers.ModelSerializer):
    """Serializer class of CartItem model for updating cart [PATCH]"""

    class Meta:
        model = CartItem
        fields = ["quantity"]

    def validate(self, data):
        """Overriding to validate cart item quantity isn't greater than actual product quantity"""
        cart_item = CartItem.objects.get(pk=self.context["pk"])
        quantity = cart_item.product.quantity

        if data["quantity"] > quantity:
            raise serializers.ValidationError(
                {"error": "Check your cart item quantity"}
            )

        return data


class CartSerializer(serializers.ModelSerializer):
    """Serializer class of Cart model [*]"""

    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "updated_at", "total_price", "items"]

    user = serializers.StringRelatedField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    def validate(self, data):
        """Override to validate one user can have only one cart"""
        user = self.context["user"]
        if Cart.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {"error": "You already have a created cart"}
            )
        return data

    def create(self, validated_data):
        """Create new cart for requested user"""
        user = self.context["user"]
        return Cart.objects.create(user=user, **validated_data)
