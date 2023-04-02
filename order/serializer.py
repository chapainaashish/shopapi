from rest_framework import serializers

from product.models import Product

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "current_price", "quantity"]

    current_price = serializers.ReadOnlyField()
    product = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        order_pk = self.context["order_pk"]
        product = Product.objects.get(pk=validated_data["product"].id)
        return OrderItem.objects.create(
            order_id=order_pk, current_price=product.price, **validated_data
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "placed_at", "delivery", "payment", "items"]

    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(read_only=True, many=True)

    def create(self, validated_data):
        user = self.context["user"]
        return Order.objects.create(user=user, **validated_data)
