from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.


@api_view(["GET"])
@permission_classes([AllowAny])
def test_view(request: Request) -> Response:
    """Test l'API avec un simple GET pour vérif."""
    return Response(
            {"message": "Hello DRF 👋"},
    )


class HelloView(APIView):
    """Test simple d'une vue nécessitant d'être authentifié."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Bonjour, vous êtes authentifié avec un token !",
            "user": request.user.username
        })