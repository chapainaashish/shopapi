from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from backends.pagination import DefaultPagination

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
    """Viewset for OrderItem model"""

    serializer_class = OrderItemSerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        items = OrderItem.objects.prefetch_related("product").filter(
            order=self.kwargs["order_pk"]
        )
        return items


class OrderViewset(ModelViewSet):
    """Viewset for Order model"""

    permission_classes = [NormalUserPermission, IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        """Returns current logged in user"""
        return {"user": self.request.user}

    def get_queryset(self):
        """Return user orders"""
        queryset = (
            Order.objects.select_related("user")
            .select_related("payment")
            .select_related("billing_address")
            .select_related("shipping_address")
            .prefetch_related("items")
            .prefetch_related("items__product")
            .all()
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user).all()

    def get_serializer_class(self):
        """Return serializer class based on request"""

        if self.request.method == "POST":
            return WriteOrderSerializer

        elif self.request.method == "PATCH":
            return UpdateOrderSerializer

        else:
            return ReadOrderSerializer


class PaymentView(RetrieveUpdateAPIView):
    """Viewset for Payment model"""

    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
