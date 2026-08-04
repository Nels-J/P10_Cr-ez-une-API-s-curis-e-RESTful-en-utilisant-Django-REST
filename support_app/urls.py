# support_app/urls.py
"""
URL configuration for softdesk project.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from support_app.views import UserViewSet

urlpatterns = [
    # Auth JWT
    path("auth/jwt/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "auth/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("auth/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),


    # Users
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user-list",
    ),
    path("users/me/", UserViewSet.as_view({"get": "retrieve"}), name="user-me"),
    path(
        "users/<int:user_id>/",
        UserViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="user-detail",
    ),
]

# TODO's
# PROJECTS :
# /projects/
# /projects/{project_id}
# /projects/{project_id}/join  # rejoindre un projet
# /projects/{project_id}/leave  # quitter un projet

# ISSUES
# /projects/{project_id}/issues/
# /projects/{project_id}/issues/{issue_id}

# COMMENTS
# /projects/{project_id}/issues/{issue_id}/comments/
# /projects/{project_id}/issues/{issue_id}/comments/{comment_id}
