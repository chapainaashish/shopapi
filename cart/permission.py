from rest_framework.permissions import IsAuthenticated


class IsCartOwner(IsAuthenticated):
    """
    Custom permission to only allow the owner of a cart to access it
    """

    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user
