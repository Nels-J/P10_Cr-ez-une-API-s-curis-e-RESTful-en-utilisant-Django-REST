from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .serializers import (
    UserUpdateSerializer,
    UserDetailSerializer,
    UserSerializer,
    ProjectSerializer,
    ProjectDetailSerializer,
    ProjectUpdateSerializer,
    ContributorSerializer, IssueSerializer,
)
from .models import User, Project, Contributor, Issue


class UserViewSet(viewsets.ModelViewSet[User]):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()  # This is the base queryset for the viewset, which will be filtered based on the action.
    lookup_url_kwarg = "user_id"  # This is the name of the URL parameter that will be used to look up individual users.

    def check_permissions(self, request: Request) -> None:
        if request.method == "POST":
            return  # Allow anyone to create a new user (registration)
        super().check_permissions(request)  # For other methods, check if the user is authenticated.

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
        return super().get_object()  # If a user_id is provided in the URL, return that user object.


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    lookup_url_kwarg = "project_id"

    def get_serializer_class(self) -> type[ProjectSerializer, ProjectDetailSerializer | ProjectUpdateSerializer]:
        if self.action == "create":
            return ProjectSerializer
        if self.action in {"update", "partial_update"}:
            return ProjectUpdateSerializer
        return ProjectDetailSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    # todo: pourrait être juste un CreateAPIView, mais on garde le ModelViewSet pour la liste des contributeurs
    permission_classes = [IsAuthenticated]
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return self.queryset.filter(project_id=self.kwargs["project_id"])

    def perform_create(self, serializer) -> None:
        serializer.save(
                project_id=self.kwargs["project_id"],
                contributor=self.request.user,
        )


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        return self.queryset.filter(project_id=self.kwargs["project_id"])  # Filter issues based on the project_id from the URL.

    def perform_create(self, serializer) -> None:
        serializer.save(
            project_id=self.kwargs["project_id"],
            author=self.request.user,
        )