from rest_framework import permissions
from rest_framework.views import Request
from .models import Product


class IsAutorizedToPostPatch(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_seller

    def has_object_permission(self, request: Request, view, obj: Product):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.seller
