from rest_framework.viewsets import ModelViewSet

from .models import Order, OrderItem, Payment
from .serializer import OrderItemSerializer, OrderSerializer, PaymentSerializer


class OrderItemViewset(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_serializer_context(self):
        return {"order_pk": self.kwargs["order_pk"]}


class OrderViewset(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_serializer_context(self):
        return {"user": self.request.user}


class PaymentViewset(ModelViewSet):
    serializer_class = PaymentSerializer

    # def get_queryset(self):
    #     queryset = Payment.objects.filter(order=self.kwargs["order_pk"])
    #     return queryset
