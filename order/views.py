from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from product.pagination import DefaultPagination

from .models import Order, OrderItem, Payment
from .permissison import NormalUserPermission
from .serializer import (
    OrderItemSerializer,
    PaymentSerializer,
    ReadOrderSerializer,
    UpdateOrderSerializer,
    WriteOrderSerializer,
)


class OrderItemViewset(ModelViewSet):
    """A viewset for OrderItem model"""

    serializer_class = OrderItemSerializer
    http_method_names = ["get", "delete"]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        items = OrderItem.objects.filter(order=self.kwargs["order_pk"])
        return items


class OrderViewset(ModelViewSet):
    """A viewset for Order model"""

    permission_classes = [NormalUserPermission]
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        """Returns current logged in user"""
        return {"user": self.request.user}

    def get_queryset(self):
        """Return order according to user"""
        if self.request.user.is_staff:
            return Order.objects.prefetch_related("items").all()

        return (
            Order.objects.prefetch_related("items").filter(user=self.request.user).all()
        )

    def get_serializer_class(self):
        """Return serializer class based on request"""

        if self.request.method == "POST":
            return WriteOrderSerializer

        elif self.request.method == "PATCH":
            return UpdateOrderSerializer

        else:
            return ReadOrderSerializer


class PaymentView(RetrieveUpdateAPIView):
    """A viewset for order payment"""

    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
