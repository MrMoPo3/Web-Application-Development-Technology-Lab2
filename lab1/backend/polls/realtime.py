from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count, Prefetch

from collaboration.consumers import POLL_UPDATES_GROUP

from .models import Choice, Poll
from .serializers import PollSerializer


def serialize_poll_for_realtime(poll_id):
    choices = Choice.objects.annotate(votes_count=Count("votes", distinct=True))
    poll = (
        Poll.objects.select_related("created_by")
        .prefetch_related(Prefetch("choices", queryset=choices))
        .annotate(total_votes=Count("votes", distinct=True))
        .get(pk=poll_id)
    )
    return PollSerializer(poll).data


def broadcast_poll_changed(action, poll_id, user=None):
    channel_layer = get_channel_layer()
    payload = {
        "type": "poll.changed",
        "action": action,
        "poll": serialize_poll_for_realtime(poll_id),
        "user": None,
    }
    if user and user.is_authenticated:
        payload["user"] = {"id": user.id, "name": user.name, "email": user.email}

    async_to_sync(channel_layer.group_send)(POLL_UPDATES_GROUP, payload)


def broadcast_poll_deleted(poll_id, user=None):
    channel_layer = get_channel_layer()
    payload = {
        "type": "poll.deleted",
        "action": "deleted",
        "poll_id": poll_id,
        "user": None,
    }
    if user and user.is_authenticated:
        payload["user"] = {"id": user.id, "name": user.name, "email": user.email}

    async_to_sync(channel_layer.group_send)(POLL_UPDATES_GROUP, payload)
