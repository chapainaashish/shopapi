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
        return item.product.price

    def get_total_price(self, item):
        return item.product.price * item.quantity

    def create(self, validated_data):
        """Overriding create method
        - Create a cart item associated with its cart
        - Update only item quantity if it's already exist in db
        """
        cart_pk = self.context["cart_pk"]
        product = validated_data["product"]

        cart_item, created = CartItem.objects.get_or_create(
            product__id=product.id, cart_id=cart_pk, defaults=validated_data
        )

        if not created:
            cart_item.quantity += validated_data["quantity"]
            cart_item.save()

        return cart_item


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "updated_at", "total_price", "items"]

    user = serializers.StringRelatedField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    def create(self, validated_data):
        user = self.context["user"]
        return Cart.objects.create(user=user, **validated_data)
