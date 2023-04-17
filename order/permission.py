from rest_framework.permissions import BasePermission, IsAuthenticated


class NormalUserPermission(IsAuthenticated):
    """Only admin user can update, normal user can only [GET, POST]"""

    def has_permission(self, request, view):
        if request.method in ("PATCH", "DELETE") and request.user.is_staff:
            return True
        return request.method in ["GET", "POST"]


class IsAuthorOrNone(BasePermission):
    """
    Custom permission to only allow methods to authorized user and admin
    """

    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user or request.user.is_staff
