from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "unit_price", "total_price"]

    unit_price = serializers.SerializerMethodField(method_name="get_unit_price")
    total_price = serializers.SerializerMethodField(method_name="get_total_price")
    # product = serializers.StringRelatedField()

    def get_unit_price(self, item):
        """Return current item price"""
        return item.product.price

    def get_total_price(self, item):
        """Return item total price"""
        return item.product.price * item.quantity

    def create(self, validated_data):
        """Add product item to the cart"""
        cart_pk = self.context["cart_pk"]
        product = validated_data["product"]

        # item already in the cart ?
        cart_item, created = CartItem.objects.get_or_create(
            product__id=product.id, cart_id=cart_pk, defaults=validated_data
        )

        # increasing the item quantity only if the item is already in the cart
        if not created:
            cart_item.quantity += validated_data["quantity"]
            cart_item.save()

        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "updated_at", "total_price", "items"]

    user = serializers.StringRelatedField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart):
        """Return total cart items price"""
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    def validate(self, attrs):
        """Override to validate one user can have only one cart"""
        user = self.context["user"]
        if Cart.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {"error": "You already have a created cart"}
            )
        return attrs

    def create(self, validated_data):
        """Create new cart for logged in user"""
        user = self.context["user"]
        return Cart.objects.create(user=user, **validated_data)
