from rest_framework.request import Request
from rest_framework.permissions import BasePermission, AllowAny

from django.contrib.auth.models import AnonymousUser


__all__ = [
    "UserHasAccess", "StaffPermission"
]


class UserHasAccess(BasePermission):
    def user_has_access(self, user) -> bool:
        return True

    def has_permission(self, request: Request, view):
        if getattr(view, "ignore_has_access", False) or (AllowAny in view.permission_classes):
            return True
        return (
            bool(request.user)
            and (not isinstance(request.user, AnonymousUser))
            and self.user_has_access(user=request.user)
        )


class StaffPermission(BasePermission):
    """
    Права для сотрудников.
    """

    def has_permission(self, request: Request, view) -> bool:
        return request.user and getattr(request.user, "is_staff", False)

    def has_object_permission(self, request: Request, view, obj) -> bool:
        return self.has_permission(request=request, view=view)
