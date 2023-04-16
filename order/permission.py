from rest_framework.permissions import BasePermission, IsAuthenticated


class NormalUserPermission(IsAuthenticated):
    """Only admin user can update order, normal user can only [GET, POST, DELETE]"""

    def has_permission(self, request, view):
        if request.method in ("PATCH", "DELETE") and request.user.is_staff:
            return True
        return request.method in ["GET", "POST"]
