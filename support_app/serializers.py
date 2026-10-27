from datetime import date
from typing import Any

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Contributor, Issue, Project, User


class UserUpdateSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        # Only allow updating the fields that are relevant for user preferences
        fields = ["can_data_be_shared", "can_be_contacted"]


class UserDetailSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        # Define fields to be included in the serialized representation of the model
        fields = [
            "id",
            "username",
            "birth_date",
            "can_data_be_shared",
            "can_be_contacted",
            "date_joined",
        ]
        # Define fields that should be read-only in the serialized representation
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
        # Ensure password is in write-only mode for security reasons
        extra_kwargs = {"password": {"write_only": True}}

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
            # Password is hashed in create_user method
            password=validated_data["password"],
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


class ProjectSerializer(serializers.ModelSerializer):
    # Automatically set the author to the currently authenticated user
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ["id", "name", "description", "category", "author", "created_time"]
        read_only_fields = ["id", "created_time"]

    @transaction.atomic
    def create(self, validated_data: Any) -> Project:
        return super().create(validated_data)


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
    # Automatically set the author to the currently authenticated user
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

    # Automatically set the project to the one specified in the URL
    def create(self, validated_data: Any) -> Issue:
        validated_data["project_id"] = self.context["view"].kwargs["project_id"]
        return super().create(validated_data)
