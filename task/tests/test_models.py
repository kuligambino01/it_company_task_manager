from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.utils import timezone

from task.models import Position, Priority, Task, TaskType


class TaskTypeModelTests(TestCase):
    def test_model_returns_str(self):
        task_type = TaskType.objects.create(name="Bug")

        self.assertEqual(str(task_type), "Bug")

    def test_name_must_be_unique(self):
        TaskType.objects.create(name="Bug")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                TaskType.objects.create(name="Bug")

    def test_cannot_delete_task_type_used_by_task(self):
        task_type = TaskType.objects.create(name="Bug")
        Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now() + timedelta(days=1),
            task_type=task_type,
        )

        with self.assertRaises(ProtectedError):
            task_type.delete()


class PositionModelTests(TestCase):
    def test_model_returns_str(self):
        position = Position.objects.create(name="QA")

        self.assertEqual(str(position), "QA")

    def test_name_must_be_unique(self):
        Position.objects.create(name="Developer")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Position.objects.create(name="Developer")

    def test_cannot_delete_position_used_by_worker(self):
        position = Position.objects.create(name="Developer")
        get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=position,
        )

        with self.assertRaises(ProtectedError):
            position.delete()


class WorkerModelTests(TestCase):
    def test_model_returns_str_with_position(self):
        position = Position.objects.create(name="Developer")
        worker = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=position,
        )

        self.assertEqual(str(worker), "test - Developer")

    def test_model_returns_str_without_position(self):
        worker = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )

        self.assertEqual(str(worker), "test")


class TaskModelTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Feature")

    def test_model_returns_str(self):
        task = Task.objects.create(
            name="Fix dashboard",
            description="Test description",
            deadline=timezone.now() + timedelta(days=1),
            task_type=self.task_type,
        )

        self.assertEqual(str(task), "Fix dashboard")

    def test_default_priority_is_medium(self):
        task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now() + timedelta(days=1),
            task_type=self.task_type,
        )

        self.assertEqual(task.priority, Priority.MEDIUM)

    def test_task_is_not_completed_by_default(self):
        task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now() + timedelta(days=1),
            task_type=self.task_type,
        )

        self.assertFalse(task.is_completed)

    def test_task_can_have_multiple_assignees(self):
        position = Position.objects.create(name="Developer")

        user_1 = get_user_model().objects.create_user(
            username="user1",
            password="test123",
            position=position,
        )
        user_2 = get_user_model().objects.create_user(
            username="user2",
            password="test123",
            position=position,
        )

        task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now() + timedelta(days=1),
            task_type=self.task_type,
        )

        task.assignees.add(user_1, user_2)

        self.assertCountEqual(
            task.assignees.all(),
            [user_1, user_2],
        )