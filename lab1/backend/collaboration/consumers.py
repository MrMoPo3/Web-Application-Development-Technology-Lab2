from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import OnlineUser
from .presence import ADMIN_ONLINE_GROUP, get_online_users_payload


POLL_UPDATES_GROUP = "poll_updates"


class PollUpdatesConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user", AnonymousUser())
        if not self.user.is_authenticated:
            await self.close(code=4401)
            return

        await self.channel_layer.group_add(POLL_UPDATES_GROUP, self.channel_name)
        await self.mark_online()
        await self.accept()
        await self.send_json({"type": "connection.accepted", "message": "Connected to PollCraft real-time updates."})
        await self.broadcast_online_users()

    async def disconnect(self, close_code):
        if getattr(self, "user", None) and self.user.is_authenticated:
            await self.channel_layer.group_discard(POLL_UPDATES_GROUP, self.channel_name)
            await self.mark_offline()
            await self.broadcast_online_users()

    async def receive_json(self, content, **kwargs):
        event_type = content.get("type")
        if event_type == "poll.focus":
            await self.channel_layer.group_send(
                POLL_UPDATES_GROUP,
                {
                    "type": "poll.focus",
                    "user": self.user_payload(),
                    "poll_id": content.get("poll_id"),
                    "message": content.get("message", ""),
                },
            )
            return

        await self.send_json({"type": "error", "message": "Unsupported event type."})

    async def poll_changed(self, event):
        await self.send_json(
            {
                "type": "poll.changed",
                "action": event["action"],
                "poll": event["poll"],
                "user": event.get("user"),
            }
        )

    async def poll_deleted(self, event):
        await self.send_json(
            {
                "type": "poll.deleted",
                "action": event["action"],
                "poll_id": event["poll_id"],
                "user": event.get("user"),
            }
        )

    async def poll_focus(self, event):
        await self.send_json(
            {
                "type": "poll.focus",
                "poll_id": event.get("poll_id"),
                "message": event.get("message"),
                "user": event.get("user"),
            }
        )

    @database_sync_to_async
    def mark_online(self):
        OnlineUser.objects.update_or_create(
            user=self.user,
            defaults={"channel_name": self.channel_name},
        )

    @database_sync_to_async
    def mark_offline(self):
        OnlineUser.objects.filter(user=self.user, channel_name=self.channel_name).delete()

    async def broadcast_online_users(self):
        await self.channel_layer.group_send(
            ADMIN_ONLINE_GROUP,
            {
                "type": "online.users.changed",
                "users": await database_sync_to_async(lambda: list(get_online_users_payload()))(),
            },
        )

    def user_payload(self):
        return {"id": self.user.id, "name": self.user.name, "email": self.user.email}


class AdminOnlineUsersConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user", AnonymousUser())
        if not self.user.is_authenticated or not self.user.is_staff:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(ADMIN_ONLINE_GROUP, self.channel_name)
        await self.accept()
        await self.send_json(
            {
                "type": "online.users.changed",
                "users": await database_sync_to_async(lambda: list(get_online_users_payload()))(),
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(ADMIN_ONLINE_GROUP, self.channel_name)

    async def online_users_changed(self, event):
        await self.send_json({"type": "online.users.changed", "users": event["users"]})
