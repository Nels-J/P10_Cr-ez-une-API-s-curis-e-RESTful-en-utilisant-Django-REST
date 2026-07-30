from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import User
from .serializers import UserSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet[User]):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def check_permissions(self, request: Request) -> None:
        if request.method == "POST":
            return
        super().check_permissions(request)

    def get_serializer_class(self) -> type[UserSerializer | UserDetailSerializer]:
        if self.request.method in ["POST"]:
            return UserSerializer
        else:
            return UserDetailSerializer
