# support_app/urls.py
"""
URL configuration for softdesk project.
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from support_app.views import UserViewSet, ProjectViewSet, ContributorViewSet

urlpatterns = [
    # Auth JWT
    path("auth/jwt/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Users
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user-list",
    ),
    path(
        "users/me/",
        UserViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="user-me",
    ),

    # Projects
    path(
        "projects/",
        ProjectViewSet.as_view({"get": "list", "post": "create"}),
        name="project-list",
    ),
    path(
        "projects/<int:project_id>/",
        ProjectViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="project-detail",
    ),

    # Contributors
    path(
        "projects/<int:project_id>/contributors/",
        ContributorViewSet.as_view({"get": "list", "post": "create"}),
        name="contributor-list",
    )

]