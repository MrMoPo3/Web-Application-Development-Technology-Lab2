from django.conf import settings
from django.db import models


class OnlineUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="online_state")
    channel_name = models.CharField(max_length=255)
    connected_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__email"]

    def __str__(self):
        return self.user.email
