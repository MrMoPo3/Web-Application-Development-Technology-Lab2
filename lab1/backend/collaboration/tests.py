from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from rest_framework.authtoken.models import Token

from pollcraft_api.asgi import application


class CollaborationWebSocketTests(TransactionTestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="online@example.com",
            password="strongpass123",
            name="Online User",
            gender="other",
            birth_date="2001-01-01",
        )
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="strongpass123",
            name="Admin User",
            gender="other",
            birth_date="1999-01-01",
            is_staff=True,
        )
        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin)

    def test_admin_receives_online_users_over_websocket(self):
        async_to_sync(self._run_online_users_flow)()

    async def _run_online_users_flow(self):
        user_communicator = WebsocketCommunicator(application, f"/ws/polls/?token={self.user_token.key}")
        user_connected, _ = await user_communicator.connect()
        self.assertTrue(user_connected)
        accepted_message = await user_communicator.receive_json_from()
        self.assertEqual(accepted_message["type"], "connection.accepted")

        admin_communicator = WebsocketCommunicator(application, f"/ws/admin/online/?token={self.admin_token.key}")
        admin_connected, _ = await admin_communicator.connect()
        self.assertTrue(admin_connected)
        online_message = await admin_communicator.receive_json_from()

        self.assertEqual(online_message["type"], "online.users.changed")
        self.assertEqual(online_message["users"][0]["email"], "online@example.com")

        await admin_communicator.disconnect()
        await user_communicator.disconnect()
