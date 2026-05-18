from rest_framework import generics, permissions

from .models import OnlineUser
from .serializers import OnlineUserSerializer


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class OnlineUserListView(generics.ListAPIView):
    serializer_class = OnlineUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return OnlineUser.objects.select_related("user").all()
