from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Address, Profile
from .serializer import ProfileSerializer, ReadAddressSerializer, WriteAddressSerializer


class ProfileViewset(ModelViewSet):
    """Viewset for user Profile model"""

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        """Overriding for getting current user profile"""
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        """Overriding for returning requested user"""
        return {"user": self.request.user, "request_method": self.request.method}


class AddressViewset(ModelViewSet):
    """Viewset for user Address model"""

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

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
