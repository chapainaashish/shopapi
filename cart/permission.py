from rest_framework.permissions import BasePermission


class IsAuthorized(BasePermission):
    """
    Custom permission to only allow view cart if requested user is authorized user
    """

    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user
