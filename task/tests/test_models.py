from django.contrib.auth import get_user_model
from django.test import TestCase

from task.models import Position, Task, TaskType


class TaskTypeModelTest(TestCase):
    def test_model_return_str(self):
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(str(task_type), "Bug")


class PositionModelTest(TestCase):
    def test_model_return_str(self):
        position = Position.objects.create(name="QA")
        self.assertEqual(str(position), "QA")


class WorkerModelTest(TestCase):
    def test_model_return_str(self):
        position = Position.objects.create(name="Developer")
        worker = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="Pawel",
            last_name="jumper",
            position=position,
        )
        self.assertEqual(str(worker), "test - Developer")


class TaskModelTest(TestCase):
    def test_model_return_str(self):
        task_type = TaskType.objects.create(name="Feature")
        task = Task.objects.create(
            name="Fix dashboard",
            description="test123",
            deadline="2026-09-26 16:00:00",
            is_completed="False",
            priority="medium",
            task_type=task_type,
        )
        self.assertEqual(str(task), "Fix dashboard")
