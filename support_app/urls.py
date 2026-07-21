# support_app/urls.py
"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from support_app.views import test_view, HelloView

urlpatterns = [
        # Test view TO DELETE WHEN TEST OK
        path("test/", test_view),

        # Auth JWT
        path("support_app/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("support_app/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

        path("support_app/hello/", HelloView.as_view()),  # Protected view for testing simplejwt token

        # API endpoints
        # todo :
        # path(
        #     "users/",
        #     UserViewSet.as_view({"get": "list", "post": "create"}),
        #     name="user-list",
        # ),
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
