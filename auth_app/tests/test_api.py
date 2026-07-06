from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse("registration")
        self.user = User.objects.create_user(
            username="basisuser", email="basis@test.de", password="password123"
        )

    def get_valid_payload(self):
        return {
            "username": "newtestuser",
            "email": "new@example.com",
            "password": "Password123!",
            "repeated_password": "Password123!",
            "type": "customer",
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.get_valid_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_duplicate_email(self):
        data = self.get_valid_payload()
        data["email"] = self.user.email
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_password_mismatch(self):
        data = self.get_valid_payload()
        data["repeated_password"] = "WrongPassword123!"
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("repeated_password", response.data)
