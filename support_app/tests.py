from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser
from django.test import TestCase  # import TestCase for testing pour unitest pas utile avec pytest a revoir.

from support_app.factory import UserFactory
from support_app.models import User

# Pour les tests, utiliser les 3 A tant que possible : Arrange, Act, Assert

# Test du endpoint auth/jwt/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"
class TokenObtainPairTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="testuser",
            password="testpassword",
            birth_date=date(1990, 1, 1),
        )

    def test_token_obtain_pair(self):
        # Arrange : préparer les données du test
        user = UserFactory.create()
        user.set_password("passworduser")
        user.save()

        # Act : appeler l'endpoint
        response = self.client.post(
            "/api/auth/jwt/create/",
            { "username": user.username, "password": "passworduser" }
        )

        # Assert : vérifier le résultat
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


# Test du endpoint auth/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"
class TokenRefreshTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="testuser",
            password="testpassword",
            birth_date=date(1990, 1, 1),
        )

    def test_token_refresh(self):
        # Arrange : obtenir un token d'accès et de rafraîchissement
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post("/api/auth/jwt/create/", login_data)
        refresh_token = response.data["refresh"]

        # Act : appeler l'endpoint de rafraîchissement
        response = self.client.post(
            "/api/auth/jwt/refresh/",
            {"refresh": refresh_token},
        )

        # Assert : vérifier le résultat
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)


# Test du endpoint auth/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"
class TokenVerifyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="testuser",
            password="testpassword",
            birth_date=date(1990, 1, 1),
        )

    def test_token_verify(self):
        # Arrange : obtenir un token d'accès
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post("/api/auth/jwt/create/", login_data)
        access_token = response.data["access"]

        # Act : appeler l'endpoint de vérification
        response = self.client.post(
            "/api/auth/jwt/verify/",
            {"token": access_token},
        )

        # Assert : vérifier le résultat
        self.assertEqual(response.status_code, 200)