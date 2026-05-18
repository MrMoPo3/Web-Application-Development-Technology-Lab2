from django.urls import path

from .consumers import AdminOnlineUsersConsumer, PollUpdatesConsumer


websocket_urlpatterns = [
    path("ws/polls/", PollUpdatesConsumer.as_asgi()),
    path("ws/admin/online/", AdminOnlineUsersConsumer.as_asgi()),
]
