from datetime import date
from typing import Any

from django.utils import timezone
from rest_framework import serializers

from .models import User


class UserUpdateSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["can_data_be_shared", "can_be_contacted"]


class UserDetailSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "username"]
        read_only_fields = ["id", "username"]


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
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}  # Ensure password is write-only

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
