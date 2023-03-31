from rest_framework import serializers

from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "placed_at", "delivery", "payment"]

    user = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        user = self.context["user"]
        return Order.objects.create(user=user, **validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "current_price", "quantity"]

    # product = serializers.StringRelatedField()
