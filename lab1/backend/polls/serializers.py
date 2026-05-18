from django.db import transaction
from rest_framework import serializers

from .models import Choice, Poll, Vote


class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Choice
        fields = ("id", "text", "votes_count")
        read_only_fields = ("id", "votes_count")


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    created_by = serializers.StringRelatedField(read_only=True)
    total_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Poll
        fields = ("id", "title", "description", "is_active", "created_by", "created_at", "choices", "total_votes")
        read_only_fields = ("id", "created_by", "created_at", "total_votes")

    def validate_choices(self, choices):
        if len(choices) < 2:
            raise serializers.ValidationError("A poll must have at least two choices.")
        return choices

    @transaction.atomic
    def create(self, validated_data):
        choices_data = validated_data.pop("choices")
        poll = Poll.objects.create(created_by=self.context["request"].user, **validated_data)
        Choice.objects.bulk_create([Choice(poll=poll, **choice) for choice in choices_data])
        return poll

    @transaction.atomic
    def update(self, instance, validated_data):
        choices_data = validated_data.pop("choices", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if choices_data is not None:
            if instance.votes.exists():
                raise serializers.ValidationError("Choices cannot be replaced after voting has started.")
            instance.choices.all().delete()
            Choice.objects.bulk_create([Choice(poll=instance, **choice) for choice in choices_data])

        return instance


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()

    def validate_choice_id(self, choice_id):
        poll = self.context["poll"]
        try:
            choice = poll.choices.get(id=choice_id)
        except Choice.DoesNotExist as exc:
            raise serializers.ValidationError("Choice does not belong to this poll.") from exc
        self.context["choice"] = choice
        return choice_id

    def validate(self, attrs):
        poll = self.context["poll"]
        user = self.context["request"].user
        if not poll.is_active:
            raise serializers.ValidationError("Poll is not active.")
        if Vote.objects.filter(poll=poll, user=user).exists():
            raise serializers.ValidationError("User has already voted in this poll.")
        return attrs

    def create(self, validated_data):
        return Vote.objects.create(
            poll=self.context["poll"],
            choice=self.context["choice"],
            user=self.context["request"].user,
        )


class PollStatsSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    total_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Poll
        fields = ("id", "title", "total_votes", "choices")
