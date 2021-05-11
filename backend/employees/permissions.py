from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'You have not enough permissions for this action '

    def has_permission(self, request, view):
        if (request.user.level == 0 or request.user.is_superuser) and request.user.is_active:
            return True
