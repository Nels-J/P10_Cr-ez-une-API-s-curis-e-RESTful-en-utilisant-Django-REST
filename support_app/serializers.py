from datetime import date
from typing import Any

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Contributor, Issue, Project, User


class UserUpdateSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["can_data_be_shared", "can_be_contacted"]


class UserDetailSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "birth_date",
            "can_data_be_shared",
            "can_be_contacted",
            "date_joined",
        ]
        read_only_fields = ["id", "username", "date_joined"]


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "birth_date",
            "can_data_be_shared",
            "can_be_contacted",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Ensure password is in write-only mode for security reasons

    def validate_birth_date(self, value: date) -> date:
        today = timezone.localdate()
        age = (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )
        if age < 15:
            raise serializers.ValidationError(
                "L'utilisateur doit avoir au moins 15 ans.",
            )
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],  # Use create_user to hash the password
            birth_date=validated_data["birth_date"],
            can_data_be_shared=validated_data.get("can_data_be_shared", False),
            can_be_contacted=validated_data.get("can_be_contacted", False),
        )
        return user


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description", "category"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "category", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time"]

# decorator to ensure that the creation of a project and its associated contributors
# is atomic, meaning that either both operations succeed or neither does, preventing
# partial updates that could lead to data inconsistencies.
@transaction.atomic
class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # Automatically set the author to the currently authenticated user

    class Meta:
        model = Project
        fields = ["id", "name", "description", "category", "author", "created_time"]
        read_only_fields = ["id", "created_time"]


class ContributorSerializer(serializers.ModelSerializer[Contributor]):
    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "created_time"]
        read_only_fields = ["id", "project", "user", "created_time"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        # Get the request object from the serializer context
        request = self.context.get("request")
        # Get the project_id from the view's URL kwargs
        project_id = self.context["view"].kwargs["project_id"]

        # Check if the user is trying to add themselves as a contributor
        if Contributor.objects.filter(
            # Check if the user requester is already a contributor to the project.
            user=request.user,
            # Check if the project_id matches the one in the URL kwargs.
            project_id=project_id,
        ).exists():
            # If the user is already a contributor, raise a validation error.
            raise serializers.ValidationError(
                "Cet utilisateur est déjà un contributeur de ce projet."
            )

        # Return the modified attrs dict to be used to create the Contributor instance.
        return attrs


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tags",
            "priority",
            "assignee",
            "status",
            "project",
            "author",
            "created_time",
        ]
        read_only_fields = ["created_time", "id", "project"]

    def create(self, validated_data):
        validated_data["project_id"] = self.context["view"].kwargs["project_id"]
        return super().create(validated_data)
