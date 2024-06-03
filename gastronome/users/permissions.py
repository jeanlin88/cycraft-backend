from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from .models import AppUser


class NotCreateAndIsObjectOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: ModelViewSet, obj):
        if (
            view.action in ['update', 'partial_update', 'destroy'] and
            obj.created_by == request.user
        ):
            return True
        raise PermissionDenied(
            "You are not owner of this object",
            code=status.HTTP_403_FORBIDDEN,
        )


class ModifyAndIsBusiness(permissions.BasePermission):
    def has_permission(self, request: Request, view: ModelViewSet):
        current_user: AppUser = request.user
        if (
            view.action in ['create', 'update', 'partial_update', 'destroy'] and
            not current_user.is_business
        ):
            raise PermissionDenied(
                "You are allowed to do this action",
                code=status.HTTP_403_FORBIDDEN,
            )
        return True


class ModifyAndIsNotBusiness(permissions.BasePermission):
    def has_permission(self, request: Request, view: ModelViewSet):
        current_user: AppUser = request.user
        if (
            view.action in ['create', 'update', 'partial_update', 'destroy'] and
            current_user.is_business
        ):
            raise PermissionDenied(
                "You are allowed to do this action",
                code=status.HTTP_403_FORBIDDEN,
            )
        return True
