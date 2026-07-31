from datetime import date
from typing import Any

from django.utils import timezone
from rest_framework import serializers

from .models import User


class UserDetailSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "username"]
        read_only_fields = ["id", "username"]


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "birth_date",
            "can_data_be_shared",
            "can_be_contacted",
        ]

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

    def save(self, **kwargs: Any) -> User:
        user = User.objects.create_user(
            username=self.validated_data["username"],
            password=self.validated_data["password"],  # Use create_user to hash the password
            birth_date=self.validated_data["birth_date"],
            can_data_be_shared=self.validated_data.get("can_data_be_shared", False),
            can_be_contacted=self.validated_data.get("can_be_contacted", False),
        )
        return user
