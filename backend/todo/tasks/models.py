"""
Task model for the todo application.

Defines the Task model with title, description, and status fields.
"""

from django.db import models


class Task(models.Model):
    """
    Task model representing a todo item.

    Attributes:
        title: Required field for task title (max 200 characters)
        description: Optional field for task description
        status: Task status with choices: 'open', 'in_progress', 'done'
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """

    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="open"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for Task model."""

        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        """Return string representation of the task."""
        return f"{self.title} ({self.status})"
