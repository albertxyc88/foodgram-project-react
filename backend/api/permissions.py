from rest_framework.permissions import SAFE_METHODS, BasePermission


class AllowAnyGetPost(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS) or (request.method == 'POST')


class CurrentUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_superuser or obj.pk == user.pk
