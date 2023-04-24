from rest_framework.permissions import BasePermission

from order.models import Order


class IsAuthorizedAndPaymentNotComplete(BasePermission):
    """
    Custom permission to only allow methods to authorized user and payment isn't completed
    """

    def has_permission(self, request, view):
        return Order.objects.filter(
            pk=view.kwargs.get("order_id"),
            payment__status__in=["P", "F"],
            user=request.user,
        ).exists()
