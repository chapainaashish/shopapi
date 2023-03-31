from rest_framework.viewsets import ModelViewSet

from .models import Order, OrderItem
from .serializer import OrderItemSerializer, OrderSerializer


class OrderItemViewset(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


class OrderViewset(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_serializer_context(self):
        return {"user": self.request.user}
