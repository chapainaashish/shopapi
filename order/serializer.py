from rest_framework import serializers

from customer.models import Address

from .models import Order, OrderItem, Payment


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "ordered_price", "quantity"]

    ordered_price = serializers.ReadOnlyField()
    # product = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "delivery",
            "payment",
            "billing_address",
            "shipping_address",
            "items",
        ]

    user = serializers.StringRelatedField(read_only=True)
    payment = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(read_only=True, many=True)
    delivery = serializers.ReadOnlyField()

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["user"]
        fields["billing_address"].queryset = Address.objects.filter(user=user)
        fields["shipping_address"].queryset = Address.objects.filter(user=user)
        return fields

    def create(self, validated_data):
        user = self.context["user"]
        order = Order.objects.create(user=user, **validated_data)
        Payment.objects.create(order=order)
        return order
