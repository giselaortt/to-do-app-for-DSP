"""
URL configuration for tasks app.

Defines the API endpoints for Task CRUD operations.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Create a router and register the TaskViewSet
router = DefaultRouter()
router.register(r"todos", TaskViewSet, basename="task")

urlpatterns = [
    path("api/", include(router.urls)),
]

