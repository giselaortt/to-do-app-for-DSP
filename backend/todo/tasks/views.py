"""
Views for the Task API.

Provides CRUD operations for Task objects using Django REST Framework.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import Http404
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task model providing CRUD operations.

    Endpoints:
        GET /api/todos/ - List all tasks
        POST /api/todos/ - Create new task
        GET /api/todos/{id}/ - Retrieve single task
        PUT /api/todos/{id}/ - Update task (full)
        PATCH /api/todos/{id}/ - Update task (partial)
        DELETE /api/todos/{id}/ - Delete task
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]  # No authentication required

    def list(self, request, *args, **kwargs):
        """
        List all tasks.

        Returns:
            Response: List of all tasks with 200 status code
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a new task.

        Returns:
            Response: Created task data with 201 status code on success,
                     error details with 400 status code on validation failure
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single task by ID.

        Returns:
            Response: Task data with 200 status code on success,
                     404 status code if task not found
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        """
        Update a task (full update).

        Returns:
            Response: Updated task data with 200 status code on success,
                     error details with 400 status code on validation failure,
                     404 status code if task not found
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a task.

        Returns:
            Response: Updated task data with 200 status code on success,
                     error details with 400 status code on validation failure,
                     404 status code if task not found
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a task.

        Returns:
            Response: Empty response with 204 status code on success,
                     404 status code if task not found
        """
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )
