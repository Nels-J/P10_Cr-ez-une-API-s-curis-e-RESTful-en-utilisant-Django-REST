# support_app/urls.py
"""
URL configuration for softdesk project.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from support_app.views import UserViewSet

urlpatterns = [
    # Auth JWT
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),


    # Users
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user-list",
    ),

    # todo :
    # path(
    #     "users/<int:user_id>/",
    #     UserViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    #     name="user-detail",
    # ),
    # /projects/
    # /projects/
    # /projects/{project_id}
    # /projects/{project_id}
    # /projects/{project_id}
    # /projects/{project_id}/issues/
    # /projects/{project_id}/issues/
    # /projects/{project_id}/issues/{issue_id}
    # /projects/{project_id}/issues/{issue_id}
    # /projects/{project_id}/issues/{issue_id}
    # /projects/{project_id}/issues/{issue_id}/comments/
    # /projects/{project_id}/issues/{issue_id}/comments/{comment_id}
    # /projects/{project_id}/issues/{issue_id}/comments/
    # /projects/{project_id}/issues/{issue_id}/comments/{comment_id}
    # /projects/{project_id}/issues/{issue_id}/comments/{comment_id}
    # /projects/{project_id}/join  # rejoindre un projet
    # /projects/{project_id}/leave  # quitter un projet
]
