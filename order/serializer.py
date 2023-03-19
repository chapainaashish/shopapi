from rest_framework import serializers

from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "placed_at", "delivery", "payment"]

    user = serializers.StringRelatedField()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "current_price", "quantity"]

    order = serializers.PrimaryKeyRelatedField()
    product = serializers.StringRelatedField()
