from django.db.models import Count, Prefetch
from rest_framework import decorators, permissions, status, viewsets
from rest_framework.response import Response

from .models import Choice, Poll
from .realtime import broadcast_poll_changed, broadcast_poll_deleted
from .serializers import PollSerializer, PollStatsSerializer, VoteSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        choices = Choice.objects.annotate(votes_count=Count("votes", distinct=True))
        return (
            Poll.objects.select_related("created_by")
            .prefetch_related(Prefetch("choices", queryset=choices))
            .annotate(total_votes=Count("votes", distinct=True))
        )

    def perform_create(self, serializer):
        poll = serializer.save()
        broadcast_poll_changed("created", poll.id, self.request.user)

    def perform_update(self, serializer):
        poll = serializer.save()
        broadcast_poll_changed("updated", poll.id, self.request.user)

    def perform_destroy(self, instance):
        poll_id = instance.id
        instance.delete()
        broadcast_poll_deleted(poll_id, self.request.user)

    @decorators.action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        poll = self.get_object()
        serializer = VoteSerializer(data=request.data, context={"request": request, "poll": poll})
        serializer.is_valid(raise_exception=True)
        vote = serializer.save()
        broadcast_poll_changed("voted", poll.id, request.user)
        return Response({"message": "Vote accepted.", "choice_id": vote.choice_id}, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def stats(self, request, pk=None):
        poll = self.get_queryset().get(pk=pk)
        serializer = PollStatsSerializer(poll)
        return Response(serializer.data)
