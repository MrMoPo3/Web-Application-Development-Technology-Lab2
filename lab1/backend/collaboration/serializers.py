from rest_framework import serializers

from .models import OnlineUser


class OnlineUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id", read_only=True)
    name = serializers.CharField(source="user.name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)

    class Meta:
        model = OnlineUser
        fields = ("id", "name", "email", "is_staff", "connected_at", "last_seen")
