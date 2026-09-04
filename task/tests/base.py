from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from task.models import Position, Priority, Task, TaskType


class BaseTaskTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=cls.position,
        )
        cls.task_type = TaskType.objects.create(name="Bug")

    def create_task(self, name, **kwargs):
        defaults = {
            "description": "Test description",
            "deadline": timezone.now() + timedelta(days=1),
            "priority": Priority.MEDIUM,
            "task_type": self.task_type,
        }
        defaults.update(kwargs)

        return Task.objects.create(
            name=name,
            **defaults,
        )