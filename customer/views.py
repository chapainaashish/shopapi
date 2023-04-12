from rest_framework.viewsets import ModelViewSet

from .models import Address, Profile
from .serializer import ProfileSerializer, ReadAddressSerializer, WriteAddressSerializer


class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {"user": self.request.user}


class AddressViewset(ModelViewSet):
    def get_queryset(self):
        queryset = Address.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadAddressSerializer
        return WriteAddressSerializer
