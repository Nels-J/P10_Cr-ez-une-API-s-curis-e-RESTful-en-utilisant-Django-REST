from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
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


# IssueViewSet with detailed schema documentation for each action.
@extend_schema_view(
    retrieve=extend_schema(
        # Summary s'affiche sur la ligne du endpoint dans la doc swagger
        summary="Retrieve issue",
        # Description s'affiche dans la doc swagger quand on clique sur l'endpoint.
        description="Retourne une issue par son id dans le contexte d'un projet.",
        # Parameters s'affiche dans la doc swagger et permet de documenter les
        # paramètres de l'URL, ici project_id et pk (id de l'issue).
        parameters=[
            OpenApiParameter(
                name="project_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="ID du projet parent",
            ),
            OpenApiParameter(
                name="pk",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="ID de l'issue",
            ),
        ],
        responses={
            200: IssueSerializer,
            403: OpenApiResponse(description="Accès refusé"),
            404: OpenApiResponse(description="Issue ou projet introuvable"),
        },
    ),
    list=extend_schema(
        description="List all issues for a specific project.",
        responses={200: IssueSerializer(many=True)},
    ),
    create=extend_schema(
        description="Create a new issue for a specific project.",
        request=IssueSerializer,
        responses={201: IssueSerializer},
    ),
    update=extend_schema(
        description="Update an existing issue. Only the author can update.",
        request=IssueSerializer,
        responses={200: IssueSerializer},
    ),
    partial_update=extend_schema(
        description="Partially update an existing issue. Only the author can update.",
        request=IssueSerializer,
        responses={200: IssueSerializer},
    ),
    destroy=extend_schema(
        description="Delete an existing issue. Only the author can delete.",
        responses={204: None},
    ),
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
    