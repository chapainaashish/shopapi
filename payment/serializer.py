from rest_framework import serializers

from .models import Payment


class ReadPaymentSerializer(serializers.ModelSerializer):
    """Serializer class of Payment model for reading payment [GET]"""

    class Meta:
        model = Payment
        fields = ["order_id", "user", "amount", "status", "created_at", "updated_at"]

    order_id = serializers.IntegerField(source="order.id")
    created_at = serializers.StringRelatedField(source="order.created_at")


class WritePaymentSerializer(serializers.ModelSerializer):
    """Serializer class of Review model for writing payment [PATCH]"""

    class Meta:
        model = Payment
        fields = ["status"]
