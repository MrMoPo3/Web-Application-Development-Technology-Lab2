from django.db.models import Count, Prefetch
from rest_framework import decorators, permissions, status, viewsets
from rest_framework.response import Response

from .models import Choice, Poll
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

    @decorators.action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        poll = self.get_object()
        serializer = VoteSerializer(data=request.data, context={"request": request, "poll": poll})
        serializer.is_valid(raise_exception=True)
        vote = serializer.save()
        return Response({"message": "Vote accepted.", "choice_id": vote.choice_id}, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def stats(self, request, pk=None):
        poll = self.get_queryset().get(pk=pk)
        serializer = PollStatsSerializer(poll)
        return Response(serializer.data)
