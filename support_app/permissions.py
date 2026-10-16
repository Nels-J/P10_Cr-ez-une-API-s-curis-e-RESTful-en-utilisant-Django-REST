from rest_framework import permissions

from support_app.models import Project


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to access it.
    """

    def has_permission(self, request, view):
        # Get the project_id from the URL kwargs
        project_id = view.kwargs.get("project_id")

        if project_id is not None:
            # Check if the user is a contributor to the project
            return Project.objects.filter(
                id=project_id,
                contributor__user=request.user
            ).exists()
        else:
            # Allow access if project_id is not provided (e.g., for list view)
            return True


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