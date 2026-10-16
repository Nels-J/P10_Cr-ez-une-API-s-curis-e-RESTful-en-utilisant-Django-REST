from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from support_app.models import Contributor, Issue, Project, User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def owner(db):
    return User.objects.create_user(
        username="owner",
        password="pass1234",
        birth_date=date(1990, 1, 1),
    )


@pytest.fixture
def other(db):
    return User.objects.create_user(
        username="other",
        password="pass1234",
        birth_date=date(1992, 1, 1),
    )


@pytest.fixture
def project(db, owner):
    return Project.objects.create(
        name="P1",
        description="desc",
        category="Back-End",
        author=owner,
    )


@pytest.mark.django_db
def test_projects_list_allowed_for_authenticated_user(api_client, other, project):
    api_client.force_authenticate(other)
    response = api_client.get(reverse("project-list"))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_project_retrieve_forbidden_if_not_contributor(api_client, other, project):
    api_client.force_authenticate(other)
    response = api_client.get(
        reverse("project-detail", kwargs={"project_id": project.id})
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_contributor_create_allows_authenticated_user_to_join(api_client, other, project):
    api_client.force_authenticate(other)
    response = api_client.post(
        reverse("contributor-list", kwargs={"project_id": project.id}),
        data={},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Contributor.objects.filter(project=project, user=other).exists()


@pytest.mark.django_db
def test_project_retrieve_allowed_after_joining(api_client, other, project):
    Contributor.objects.create(project=project, user=other, role="Contributor")
    api_client.force_authenticate(other)
    response = api_client.get(
        reverse("project-detail", kwargs={"project_id": project.id})
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_issue_update_forbidden_for_contributor_if_not_author(
    api_client, owner, other, project
):
    Contributor.objects.create(project=project, user=other, role="Contributor")
    issue = Issue.objects.create(
        title="I1",
        description="d",
        project=project,
        author=owner,
        status="To Do",
    )

    api_client.force_authenticate(other)
    response = api_client.patch(
        reverse("issue-detail", kwargs={"project_id": project.id, "pk": issue.id}),
        data={"title": "new"},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_issue_update_allowed_for_author(api_client, owner, project):
    issue = Issue.objects.create(
        title="I1",
        description="d",
        project=project,
        author=owner,
        status="To Do",
    )

    api_client.force_authenticate(owner)
    response = api_client.patch(
        reverse("issue-detail", kwargs={"project_id": project.id, "pk": issue.id}),
        data={"title": "new"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK