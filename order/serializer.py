from django.db import transaction
from rest_framework import serializers

from cart.models import Cart, CartItem
from customer.models import Address
from customer.serializer import ReadAddressSerializer
from payment.models import Payment
from payment.serializer import ReadPaymentSerializer
from product.models import Product

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer class of OrderItem model[*]"""

    class Meta:
        model = OrderItem
        fields = ["id", "product", "ordered_price", "quantity", "total_price"]

    ordered_price = serializers.ReadOnlyField()
    product = serializers.StringRelatedField()


class ReadOrderSerializer(serializers.ModelSerializer):
    """Serializer class of Order model for reading order [GET]"""

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "delivery",
            "payment",
            "total_price",
            "billing_address",
            "shipping_address",
            "items",
        ]

    user = serializers.StringRelatedField()
    payment = ReadPaymentSerializer()
    items = OrderItemSerializer(many=True)
    billing_address = ReadAddressSerializer()
    shipping_address = ReadAddressSerializer()


class UpdateOrderSerializer(serializers.ModelSerializer):
    """Serializer class of Order model for updating order [PATCH]"""

    class Meta:
        model = Order
        fields = ["delivery"]


class WriteOrderSerializer(serializers.Serializer):
    """Serializer class for Order model for writing order [POST]"""

    cart_id = serializers.IntegerField()
    billing_address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.none()
    )
    shipping_address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.none()
    )

    # user can only choose his/her address from Address table while ordering
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get("user")
        self.fields["billing_address"].queryset = Address.objects.filter(user=user)
        self.fields["shipping_address"].queryset = Address.objects.filter(user=user)

    def validate(self, attrs):
        """Validate whether the cart exists and contains items"""
        cart = Cart.objects.filter(
            pk=attrs.get("cart_id"), user=self.context.get("user")
        )

        if not cart.exists():
            raise serializers.ValidationError({"error": "invalid cart"})

        if cart.first().items.count() < 1:
            raise serializers.ValidationError({"error": "no item added to the cart"})

        return attrs

    def save(self, **kwargs):
        """Create an order of the user from the submitted cart"""

        #  current user and his/her cart id
        user = self.context.get("user")
        cart_id = self.validated_data.get("cart_id")
        cart = Cart.objects.filter(pk=cart_id, user=user)

        with transaction.atomic():
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

            # updating product quantity after order
            # assuming shopapi supports 'cash on delivery'
            # you can move this logic to StripeWebhook view instead
            for item in cart_items:
                product = Product.objects.get(pk=item.product.id)
                if product.quantity < item.quantity:
                    raise serializers.ValidationError(
                        {
                            "error": "You can't order more than product quantity, Please check the quantity first"
                        }
                    )
                product.quantity = product.quantity - item.quantity
                product.save()

            OrderItem.objects.bulk_create(order_items)
            cart.delete()
