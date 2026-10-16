import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from support_app.factory import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    user = UserFactory.create()
    user.set_password("pass1234")
    user.save()
    return user


@pytest.fixture
def jwt_tokens(api_client, user):
    response = api_client.post(
        reverse("token_obtain_pair"),
        data={"username": user.username, "password": "pass1234"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    return response.data


@pytest.fixture
def auth_client(api_client, jwt_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_tokens['access']}")
    return api_client


@pytest.mark.django_db
def test_jwt_create_returns_tokens(api_client, user):
    response = api_client.post(
        reverse("token_obtain_pair"),
        data={"username": user.username, "password": "pass1234"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_jwt_create_fails_with_bad_credentials(api_client, user):
    response = api_client.post(
        reverse("token_obtain_pair"),
        data={"username": user.username, "password": "wrong-password"},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_projects_list_requires_authentication(api_client):
    response = api_client.get(reverse("project-list"))
    assert response.status_code in {
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    }


@pytest.mark.django_db
def test_projects_list_works_with_valid_jwt(auth_client):
    response = auth_client.get(reverse("project-list"))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_jwt_refresh_returns_new_access(api_client, jwt_tokens):
    response = api_client.post(
        reverse("token_refresh"),
        data={"refresh": jwt_tokens["refresh"]},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_jwt_verify_accepts_valid_access(api_client, jwt_tokens):
    response = api_client.post(
        reverse("token_verify"),
        data={"token": jwt_tokens["access"]},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK