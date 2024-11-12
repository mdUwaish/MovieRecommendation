from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsMovieOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.method == 'PUT' or request.method == 'DELETE':
                return obj.moderator == request.user or request.user.role == 'Admin'
        return False


class IsReviewOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user