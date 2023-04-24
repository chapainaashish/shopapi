from rest_framework.permissions import BasePermission

from order.models import Order


class IsAuthorizedOrNone(BasePermission):
    """
    Custom permission to only allow methods to authorized user and admin
    """

    def has_permission(self, request, view):
        order = Order.objects.get(pk=view.kwargs.get("order_id"))
        return order.user == request.user
