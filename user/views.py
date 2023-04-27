from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Address, Profile
from .serializer import ProfileSerializer, ReadAddressSerializer, WriteAddressSerializer


class ProfileViewset(ModelViewSet):
    """A viewset for User Profile model"""

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """Overriding for getting current user profile"""
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        """Overriding for returning requested user"""
        return {"user": self.request.user, "request_method": self.request.method}


class AddressViewset(ModelViewSet):
    """A viewset for User Address model"""

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "post", "patch", "delete"]

    def get_queryset(self):
        """Overriding for getting current user address"""
        queryset = Address.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        """Overriding for returning requested user"""
        return {"user": self.request.user}

    def get_serializer_class(self):
        """Overriding to return serializer class based on HTTP method"""
        if self.request.method == "GET":
            return ReadAddressSerializer
        return WriteAddressSerializer
