from datetime import date
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Comment, Contributor, Issue, Project, User


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assignee_field = self.fields.get("assignee")
        if not isinstance(assignee_field, serializers.PrimaryKeyRelatedField):
            return

        view = self.context.get("view")

        project_id = getattr(view, "kwargs", {}).get("project_id") if view else None
        if project_id is None and self.instance is not None:
            project_id = self.instance.project_id

        # If project_id is still None, set the queryset to none
        if project_id is None:
            assignee_field.queryset = User.objects.none()
            return

        # Set the queryset to only include users who are contributors to the project
        assignee_field.queryset = User.objects.filter(
            contributions__project_id=project_id
        ).distinct()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        # Validate that the assignee is a contributor to the project
        project = attrs.get("project")
        if project is None and self.instance is not None:
            project = self.instance.project

        # If project is still None, try to get it from the view context
        if project is None:
            view = self.context.get("view")
            project_id = getattr(view, "kwargs", {}).get("project_id") if view else None
            if project_id is not None:
                project = Project.objects.filter(pk=project_id).first()

        assignee = attrs.get("assignee")
        if "assignee" not in attrs and self.instance is not None:
            assignee = self.instance.assignee

        issue = Issue(project=project, assignee=assignee)
        try:
            issue.clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc

        return attrs

    # Automatically set the project to the one specified in the URL
    def create(self, validated_data: Any) -> Issue:
        validated_data["project_id"] = self.context["view"].kwargs["project_id"]
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    # Automatically set the author to the currently authenticated user
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ["id", "uuid", "content", "author", "issue", "created_time"]
        read_only_fields = ["id", "uuid", "created_time", "issue"]

    # Automatically set the issue to the one specified in the URL
    def create(self, validated_data: Any) -> Comment:
        validated_data["issue_id"] = self.context["view"].kwargs["issue_id"]
        return super().create(validated_data)