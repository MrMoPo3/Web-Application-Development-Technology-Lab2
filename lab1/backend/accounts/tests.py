from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthApiTests(APITestCase):
    def test_register_login_and_profile(self):
        register_response = self.client.post(
            reverse("register"),
            {
                "name": "Olena User",
                "email": "olena@example.com",
                "gender": "female",
                "birth_date": "2002-04-12",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", register_response.data)

        login_response = self.client.post(
            reverse("login"),
            {"email": "olena@example.com", "password": "strongpass123"},
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {login_response.data['token']}")
        profile_response = self.client.get(reverse("profile"))

        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["email"], "olena@example.com")
