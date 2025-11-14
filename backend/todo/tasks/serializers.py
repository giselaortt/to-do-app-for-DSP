"""
Serializers for the Task model.

Provides serialization and validation for Task objects.
"""

from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.

    Handles serialization, deserialization, and validation of Task objects.
    """

    class Meta:
        """Meta configuration for TaskSerializer."""

        model = Task
        fields = ["id", "title", "description", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        """
        Validate that title is not empty or only whitespace.

        Args:
            value: The title value to validate

        Returns:
            str: The validated title

        Raises:
            serializers.ValidationError: If title is empty or only whitespace
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_status(self, value):
        """
        Validate that status is one of the allowed choices.

        Args:
            value: The status value to validate

        Returns:
            str: The validated status

        Raises:
            serializers.ValidationError: If status is not a valid choice
        """
        valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}"
            )
        return value

