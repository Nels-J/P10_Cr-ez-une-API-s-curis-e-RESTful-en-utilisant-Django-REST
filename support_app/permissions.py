from rest_framework import permissions

from support_app.models import Project


class IsContributor(permissions.BasePermission):
    # Custom permission to only allow contributors of a project to access it.
    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")
        if project_id is None:
            return True
        return Project.objects.filter(
            id=project_id,
            contributor__user=request.user,
        ).exists()


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if the user is the author of the object
        return obj.author == request.user