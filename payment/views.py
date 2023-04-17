from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from backends.permission import IsAdminOrReadOnly

from .models import Payment
from .serializer import ReadPaymentSerializer, WritePaymentSerializer


class PaymentViewset(ModelViewSet):
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.select_related("order").filter()
        return Payment.objects.select_related("order").filter(
            order__user=self.request.user
        )

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return WritePaymentSerializer
        return ReadPaymentSerializer
