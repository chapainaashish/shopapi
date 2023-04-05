from rest_framework import serializers

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
            "items",
        ]

    user = serializers.StringRelatedField(read_only=True)
    payment = PaymentSerializer(read_only=True)
    items = OrderItemSerializer(read_only=True, many=True)

    def create(self, validated_data):
        user = self.context["user"]
        order = Order.objects.create(user=user, **validated_data)
        Payment.objects.create(order=order)
        return order
