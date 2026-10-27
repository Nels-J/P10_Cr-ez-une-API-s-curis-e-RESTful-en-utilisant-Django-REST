from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import Comment, Contributor, Issue, Project, User
from .permissions import IsAuthor, IsContributor
from .serializers import (
    CommentSerializer,
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

    queryset = User.objects.all()
    lookup_url_kwarg = "user_id"

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
            return UserSerializer
        if self.action in {"update", "partial_update"}:
            return UserUpdateSerializer
        return UserDetailSerializer

    def get_object(self):
        if self.kwargs.get(self.lookup_url_kwarg) is None:
            return self.request.user  # Return the currently authenticated user.
        return (
            super().get_object()
        )  # If a user_id is provided in the URL, return that user object.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("-created_time")
    lookup_url_kwarg = "project_id"

    # Custom permission handling based on the action being performed.
    def get_permissions(self):
        if self.action in {"list", "create"}:
            return [IsAuthenticated()]
        if self.action == "retrieve":
            return [IsAuthenticated(), IsContributor()]
        if self.action in {"update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsContributor(), IsAuthor()]
        return [IsAuthenticated()]

    def get_serializer_class(
        self,
    ) -> type[ProjectSerializer, ProjectDetailSerializer | ProjectUpdateSerializer]:
        if self.action == "create":
            return ProjectSerializer
        if self.action in {"update", "partial_update"}:
            return ProjectUpdateSerializer
        return ProjectDetailSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    # Custom permission handling based on the action being performed.
    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsContributor()]

    def get_queryset(self):
        # Filter contributors by the project_id from the URL kwargs
        # and order them by created_time in descending order.
        return self.queryset.filter(project_id=self.kwargs["project_id"]).order_by(
            "-created_time"
        )

    def perform_create(self, serializer) -> None:
        serializer.save(
            project_id=self.kwargs["project_id"],
            user=self.request.user,
        )


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action in {"update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsContributor(), IsAuthor()]
        return [IsAuthenticated(), IsContributor()]

    def get_queryset(self):
        # Filter issues by the project_id from the URL kwargs
        # and order them by created_time in descending order.
        return self.queryset.filter(project_id=self.kwargs["project_id"]).order_by(
            "-created_time"
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in {"update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsContributor(), IsAuthor()]
        return [IsAuthenticated(), IsContributor()]

    def get_queryset(self):
        # Filter comments by the issue_id from the URL kwargs
        # and order them by created_time in descending order.
        return self.queryset.filter(issue_id=self.kwargs["issue_id"]).order_by(
            "-created_time"
        )
    