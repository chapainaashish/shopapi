from rest_framework import serializers, status
from rest_framework.response import Response

from cart.models import Cart, CartItem
from customer.models import Address

from .models import Order, OrderItem, Payment


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "ordered_price", "quantity"]

    ordered_price = serializers.ReadOnlyField()
    # product = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        """Add item to the associated order"""
        order_pk = self.context["order_pk"]
        return OrderItem.objects.create(
            order_id=order_pk,
            ordered_price=validated_data["product"].price,
            **validated_data
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["order", "status", "updated_at"]

    order = serializers.ReadOnlyField(source="order.id")


class ReadOrderSerializer(serializers.ModelSerializer):
    """Serializer for Order GET request"""

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "billing_address",
            "shipping_address",
            "delivery",
            "payment",
            "items",
        ]

    user = serializers.StringRelatedField(read_only=True)
    payment = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(read_only=True, many=True)
    delivery = serializers.ReadOnlyField()


# get cart id and check if it's belongs to the user
# create a new order and move cart items to order items
class WriteOrderSerializer(serializers.Serializer):
    """Serializer for Order POST request"""

    cart_id = serializers.IntegerField()
    billing_address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.none()
    )
    shipping_address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.none()
    )

    # so that, user can only choose his/her address from Address table while ordering
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get("user")
        self.fields["billing_address"].queryset = Address.objects.filter(user=user)
        self.fields["shipping_address"].queryset = Address.objects.filter(user=user)

    def save(self, **kwargs):
        """Create an order from the cart"""

        #  current user and his/her cart id
        user = self.context.get("user")
        cart_id = self.validated_data.get("cart_id")
        cart = Cart.objects.filter(pk=cart_id, user=user)

        # if the cart belongs to the user
        if cart.exists():
            order = Order.objects.create(
                user=user,
                billing_address=self.validated_data["billing_address"],
                shipping_address=self.validated_data["shipping_address"],
            )
            Payment.objects.get_or_create(order=order)

            # moving cart items to order items and deleting cart
            cart_items = CartItem.objects.filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    ordered_price=item.product.price,
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            cart.delete()

        else:
            raise serializers.ValidationError({"error": "invalid cart"})
