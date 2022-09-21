from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """Full access for admin and superuser only."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    """
    List permission for authenticated, obj permission
    for admin and moderator, or read only.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdmin(permissions.BasePermission):
    """Create and delete access for admin, read for everyone."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.method in permissions.SAFE_METHODS)
