from rest_framework import permissions
from rest_framework.views import Request, Response, status
from users.models import User




class IsAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request: Request, view, obj: User):             

        return request.user == obj


