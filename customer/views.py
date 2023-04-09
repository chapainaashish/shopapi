from rest_framework.viewsets import ModelViewSet

from .models import Address, Profile
from .serializer import AddressSerializer, ProfileSerializer


class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {"user": self.request.user}


class AddressViewset(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        queryset = Address.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {"user": self.request.user}
