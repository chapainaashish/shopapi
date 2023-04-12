from rest_framework.permissions import IsAuthenticated


class NormalUserPermission(IsAuthenticated):
    """Only admin user can update order, normal user can only [GET, POST, DELETE]"""

    def has_permission(self, request, view):
        if request.method == "PATCH" and request.user.is_staff:
            return True
        return request.method in ["GET", "POST", "DELETE"]
