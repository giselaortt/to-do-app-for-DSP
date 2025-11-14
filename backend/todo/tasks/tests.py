"""
Tests for Task model, serializer, and API endpoints.

Comprehensive test coverage for all CRUD operations and edge cases.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task


class TaskModelTest(TestCase):
    """Test cases for Task model."""

    def setUp(self):
        """Set up test fixtures."""
        self.task = Task.objects.create(
            title="Test Task", description="Test Description", status="open"
        )

    def test_task_creation(self):
        """Test that a task can be created with all fields."""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertEqual(self.task.status, "open")
        self.assertIsNotNone(self.task.id)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)

    def test_task_str_representation(self):
        """Test the string representation of a task."""
        expected = f"Test Task (open)"
        self.assertEqual(str(self.task), expected)

    def test_task_default_status(self):
        """Test that default status is 'open'."""
        task = Task.objects.create(title="New Task")
        self.assertEqual(task.status, "open")

    def test_task_ordering(self):
        """Test that tasks are ordered by created_at descending."""
        task1 = Task.objects.create(title="First Task")
        task2 = Task.objects.create(title="Second Task")
        tasks = list(Task.objects.all())
        # Most recent first
        self.assertEqual(tasks[0].title, "Second Task")
        self.assertEqual(tasks[1].title, "First Task")


class TaskSerializerTest(TestCase):
    """Test cases for TaskSerializer."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()

    def test_valid_task_serialization(self):
        """Test serialization of a valid task."""
        task = Task.objects.create(
            title="Test Task", description="Description", status="open"
        )
        from .serializers import TaskSerializer

        serializer = TaskSerializer(task)
        data = serializer.data
        self.assertEqual(data["title"], "Test Task")
        self.assertEqual(data["description"], "Description")
        self.assertEqual(data["status"], "open")
        self.assertIn("id", data)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_empty_title_validation(self):
        """Test that empty title raises validation error."""
        from .serializers import TaskSerializer

        serializer = TaskSerializer(data={"title": "", "status": "open"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_whitespace_only_title_validation(self):
        """Test that whitespace-only title raises validation error."""
        from .serializers import TaskSerializer

        serializer = TaskSerializer(data={"title": "   ", "status": "open"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_invalid_status_validation(self):
        """Test that invalid status raises validation error."""
        from .serializers import TaskSerializer

        serializer = TaskSerializer(
            data={"title": "Test", "status": "invalid_status"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_valid_status_choices(self):
        """Test that all valid status choices are accepted."""
        from .serializers import TaskSerializer

        for status_choice in ["open", "in_progress", "done"]:
            serializer = TaskSerializer(
                data={"title": "Test", "status": status_choice}
            )
            self.assertTrue(serializer.is_valid(), f"Status {status_choice} should be valid")


class TaskAPITest(TestCase):
    """Test cases for Task API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.task = Task.objects.create(
            title="Test Task", description="Test Description", status="open"
        )
        self.list_url = reverse("task-list")
        self.detail_url = reverse("task-detail", kwargs={"pk": self.task.id})

    def test_list_tasks(self):
        """Test GET /api/todos/ returns list of tasks."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Task")

    def test_create_task(self):
        """Test POST /api/todos/ creates a new task."""
        data = {
            "title": "New Task",
            "description": "New Description",
            "status": "in_progress",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Task")
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_without_description(self):
        """Test POST /api/todos/ creates task without description."""
        data = {"title": "Task Without Description", "status": "open"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Task Without Description")
        self.assertIsNone(response.data["description"])

    def test_create_task_missing_title(self):
        """Test POST /api/todos/ returns 400 when title is missing."""
        data = {"description": "Description without title"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_task_empty_title(self):
        """Test POST /api/todos/ returns 400 when title is empty."""
        data = {"title": "", "status": "open"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_task(self):
        """Test GET /api/todos/{id}/ returns a single task."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Task")
        self.assertEqual(response.data["id"], self.task.id)

    def test_retrieve_nonexistent_task(self):
        """Test GET /api/todos/{id}/ returns 404 for non-existent task."""
        url = reverse("task-detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_put(self):
        """Test PUT /api/todos/{id}/ updates a task."""
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "done",
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Task")
        self.assertEqual(response.data["status"], "done")
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_update_task_patch(self):
        """Test PATCH /api/todos/{id}/ partially updates a task."""
        data = {"status": "in_progress"}
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "in_progress")
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "in_progress")
        # Title should remain unchanged
        self.assertEqual(self.task.title, "Test Task")

    def test_update_nonexistent_task(self):
        """Test PUT /api/todos/{id}/ returns 404 for non-existent task."""
        url = reverse("task-detail", kwargs={"pk": 99999})
        data = {"title": "Updated", "status": "open"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_invalid_status(self):
        """Test PUT /api/todos/{id}/ returns 400 for invalid status."""
        data = {"title": "Test", "status": "invalid_status"}
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)

    def test_delete_task(self):
        """Test DELETE /api/todos/{id}/ deletes a task."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_nonexistent_task(self):
        """Test DELETE /api/todos/{id}/ returns 404 for non-existent task."""
        url = reverse("task-detail", kwargs={"pk": 99999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_multiple_tasks_list(self):
        """Test listing multiple tasks."""
        Task.objects.create(title="Task 2", status="in_progress")
        Task.objects.create(title="Task 3", status="done")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
