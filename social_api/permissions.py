from rest_framework.permissions import BasePermission


class IsOwnerReadOnly(BasePermission):
    """Allow access only for the owner of the object."""

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.owner == request.user
