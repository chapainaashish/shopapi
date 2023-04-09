from rest_framework.viewsets import ModelViewSet

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


class CartViewset(ModelViewSet):
    serializer_class = CartSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_queryset(self):
        queryset = Cart.objects.prefetch_related("items").filter(user=self.request.user)
        return queryset


class CartItemViewset(ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def get_queryset(self):
        items = CartItem.objects.filter(cart=self.kwargs["cart_pk"])
        return items

    def get_serializer_context(self):
        return {"cart_pk": self.kwargs["cart_pk"]}
