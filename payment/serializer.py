from rest_framework import serializers

from .models import Payment


class ReadPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["order_id", "order", "status", "updated_at"]

    order_id = serializers.IntegerField(source="order.id")
    order = serializers.StringRelatedField(source="order.created_at")


class WritePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["status"]
