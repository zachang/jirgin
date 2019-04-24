from rest_framework.permissions import BasePermission, SAFE_METHODS 


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow only owners of an object to modify it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return obj.id == request.user.id

        # Write permissions are only allowed to the owner of the data.
        return obj.id == request.user.id