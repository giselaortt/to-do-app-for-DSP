"""
Admin configuration for Task model.

Registers Task model in Django admin interface.
"""

from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for Task model.

    Displays task fields in the admin interface with filtering and search.
    """

    list_display = ["id", "title", "status", "created_at", "updated_at"]
    list_filter = ["status", "created_at", "updated_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
