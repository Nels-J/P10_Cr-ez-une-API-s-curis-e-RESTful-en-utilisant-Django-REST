from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import Contributor, Issue, Project, User
from .permissions import IsAuthor, IsContributor
from .serializers import (
    ContributorSerializer,
    IssueSerializer,
    ProjectDetailSerializer,
    ProjectSerializer,
    ProjectUpdateSerializer,
    UserDetailSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet[User]):
    permission_classes = [IsAuthenticated]
    # surcharge the default pagination to display 2 users per page.
    # todo check

    queryset = (
        User.objects.all()
    )  # The base queryset for viewset, which will be filtered based on the action.
    lookup_url_kwarg = "user_id"  # The parameter name on the URL that will be used to look up individual users.

    def check_permissions(self, request: Request) -> None:
        if request.method == "POST":
            return  # Allow anyone to create a new user (registration)
        super().check_permissions(
            request
        )  # For other methods, check if the user is authenticated.

    def get_serializer_class(
        self,
    ) -> type[UserSerializer, UserDetailSerializer | UserUpdateSerializer]:
        if self.action == "create":
            return UserSerializer  # For "create" action, use the UserSerializer.
        if self.action in {"update", "partial_update"}:
            return UserUpdateSerializer  # For "update" and "partial_update" actions, use the UserUpdateSerializer.
        return UserDetailSerializer  # For "list" and "retrieve" actions, use the UserDetailSerializer.

    def get_object(self):
        if self.kwargs.get(self.lookup_url_kwarg) is None:
            return self.request.user  # Return the currently authenticated user.
        return (
            super().get_object()
        )  # If a user_id is provided in the URL, return that user object.


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        IsContributor,
    ]  # Only authenticated users who are contributors can access this viewset.
    queryset = Project.objects.all()
    lookup_url_kwarg = "project_id"

    def get_serializer_class(
        self,
    ) -> type[ProjectSerializer, ProjectDetailSerializer | ProjectUpdateSerializer]:
        if self.action == "create":
            return ProjectSerializer
        if self.action in {"update", "partial_update"}:
            return ProjectUpdateSerializer
        return ProjectDetailSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return self.queryset.filter(project_id=self.kwargs["project_id"])

    def perform_create(self, serializer) -> None:
        serializer.save(
            project_id=self.kwargs["project_id"],
            user=self.request.user,
        )


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        IsContributor,
        IsAuthor,
    ]  # only authenticated users can access this viewset, and they must be contributor or author of the issue.
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        return self.queryset.filter(
            project_id=self.kwargs["project_id"]
        )  # Filter issues based on the project_id from the URL.

    def perform_create(self, serializer) -> None:
        serializer.save(
            project_id=self.kwargs["project_id"],
            author=self.request.user,
        )
