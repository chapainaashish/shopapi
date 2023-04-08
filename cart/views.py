from rest_framework.viewsets import ModelViewSet

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


class CartViewset(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartItemViewset(ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
