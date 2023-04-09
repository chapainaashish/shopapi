from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Order, OrderItem, Payment
from .serializer import OrderItemSerializer, OrderSerializer, PaymentSerializer


class OrderItemViewset(ModelViewSet):
    serializer_class = OrderItemSerializer

    def get_serializer_context(self):
        return {"order_pk": self.kwargs["order_pk"]}

    def get_queryset(self):
        items = OrderItem.objects.filter(order=self.kwargs["order_pk"])
        return items


class OrderViewset(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related("items").all()

    def get_serializer_context(self):
        return {"user": self.request.user}


class PaymentView(RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


"""
class PaymentViewset(ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.filter(order=self.kwargs["order_pk"])
        return queryset
"""
