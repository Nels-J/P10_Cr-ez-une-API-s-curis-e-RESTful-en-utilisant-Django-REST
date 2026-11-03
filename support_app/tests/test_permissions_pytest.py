import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from support_app.factory import UserFactory
from support_app.models import Contributor, Issue, Project


# FIXTURES - Used to set up test environment & reusable components for testing.
@pytest.fixture
def api_client():
    # Create an instance of the APIClient for testing
    # This fixture will be used in the tests to make API requests.
    return APIClient()


@pytest.fixture
def owner(db):
    # Create a user with the username "owner"
    # This fixture will be used to represent the owner of a project in the tests.
    return UserFactory(username="owner")


@pytest.fixture
def other(db):
    # Create a user with the username "other"
    # This fixture will be used to represent another user in the tests.
    return UserFactory(username="other")


@pytest.fixture
def project(db, owner):
    # Create a project with the owner as the author
    # This fixture will be used to represent a project in the tests.
    return Project.objects.create(
        name="P1",
        description="desc",
        category="Back-End",
        author=owner,
    )


# TESTS CASES
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
def test_contributor_create_allows_authenticated_user_to_join(
    api_client, other, project
):
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


@pytest.mark.django_db
def test_issue_create_rejects_assignee_when_not_project_contributor(
    api_client, owner, other, project
):
    api_client.force_authenticate(owner)
    response = api_client.post(
        reverse("issue-list", kwargs={"project_id": project.id}),
        data={
            "title": "I1",
            "description": "d",
            "status": "To Do",
            "assignee": other.id,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "assignee" in response.data


@pytest.mark.django_db
def test_issue_patch_accepts_assignee_when_project_contributor(
    api_client, owner, other, project
):
    issue = Issue.objects.create(
        title="I1",
        description="d",
        project=project,
        author=owner,
        status="To Do",
    )
    Contributor.objects.create(project=project, user=other, role="Contributor")

    api_client.force_authenticate(owner)
    response = api_client.patch(
        reverse("issue-detail", kwargs={"project_id": project.id, "pk": issue.id}),
        data={"assignee": other.id},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_issue_patch_accepts_null_assignee(api_client, owner, project):
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
        data={"assignee": None},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
