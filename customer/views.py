from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from backends.permission import IsAdminOrReadOnly
from order.models import Payment

from .models import Address, Profile
from .serializer import (
    ProfileSerializer,
    ReadAddressSerializer,
    ReadPaymentSerializer,
    WriteAddressSerializer,
    WritePaymentSerializer,
)


class ProfileViewset(ModelViewSet):
    """Viewset for user Profile model"""

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Overriding for getting current user profile"""
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        """Overriding for returning requested user"""
        return {"user": self.request.user}


class AddressViewset(ModelViewSet):
    """Viewset for user Address model"""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Overriding for getting current user address"""
        queryset = Address.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        """Overriding for returning requested user"""
        return {"user": self.request.user}

    def get_serializer_class(self):
        """Returning serializer class based on HTTP request method"""
        if self.request.method == "GET":
            return ReadAddressSerializer
        return WriteAddressSerializer


class PaymentViewset(ModelViewSet):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return WritePaymentSerializer
        return ReadPaymentSerializer
