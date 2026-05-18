from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import OnlineUser
from .serializers import OnlineUserSerializer


ADMIN_ONLINE_GROUP = "admin_online_users"


def get_online_users_payload():
    users = OnlineUser.objects.select_related("user").all()
    return OnlineUserSerializer(users, many=True).data


def broadcast_online_users():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        ADMIN_ONLINE_GROUP,
        {
            "type": "online.users.changed",
            "users": list(get_online_users_payload()),
        },
    )
