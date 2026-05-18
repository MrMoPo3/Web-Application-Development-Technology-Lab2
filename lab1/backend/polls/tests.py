from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class PollApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="creator@example.com",
            password="strongpass123",
            name="Creator",
            gender="other",
            birth_date="2000-01-01",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_about_poll_create_vote_and_stats(self):
        about_response = self.client.get(reverse("about-app"))
        self.assertEqual(about_response.status_code, status.HTTP_200_OK)
        self.assertEqual(about_response.data["name"], "PollCraft")

        poll_response = self.client.post(
            reverse("poll-list"),
            {
                "title": "Best framework?",
                "description": "Choose one option.",
                "is_active": True,
                "choices": [{"text": "Django"}, {"text": "Flask"}],
            },
            format="json",
        )

        self.assertEqual(poll_response.status_code, status.HTTP_201_CREATED)
        poll_id = poll_response.data["id"]
        choice_id = poll_response.data["choices"][0]["id"]

        vote_response = self.client.post(
            reverse("poll-vote", args=[poll_id]),
            {"choice_id": choice_id},
            format="json",
        )

        self.assertEqual(vote_response.status_code, status.HTTP_201_CREATED)

        stats_response = self.client.get(reverse("poll-stats", args=[poll_id]))
        self.assertEqual(stats_response.status_code, status.HTTP_200_OK)
        self.assertEqual(stats_response.data["total_votes"], 1)
        self.assertEqual(stats_response.data["choices"][0]["votes_count"], 1)
