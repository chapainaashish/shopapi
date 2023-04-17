from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from backends.pagination import DefaultPagination
from backends.permission import IsAdminOrReadOnly

from .models import Order, OrderItem
from .permission import IsAuthorOrNone, NormalUserPermission
from .serializer import (
    OrderItemSerializer,
    ReadOrderSerializer,
    UpdateOrderSerializer,
    WriteOrderSerializer,
)


class OrderItemViewset(ModelViewSet):
    """A viewset for OrderItem model"""

    serializer_class = OrderItemSerializer
    http_method_names = ["get", "delete"]
    permission_classes = [IsAuthenticated, IsAuthorOrNone, IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_queryset(self):
        """Overriding to return user specific order"""

        if self.request.user.is_staff:
            return OrderItem.objects.prefetch_related("product").filter(
                order=self.kwargs["order_pk"]
            )
        return OrderItem.objects.prefetch_related("product").filter(
            order=self.kwargs["order_pk"], order__user=self.request.user
        )


class OrderViewset(ModelViewSet):
    """A viewset for Order model"""

    permission_classes = [NormalUserPermission, IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        """Overriding to return requested user"""
        return {"user": self.request.user}

    def get_queryset(self):
        """Overriding to return user specific order"""
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
        """Overriding to return serializer class based on HTTP method"""

        if self.request.method == "POST":
            return WriteOrderSerializer

        if self.request.method == "PATCH":
            return UpdateOrderSerializer

        return ReadOrderSerializer
