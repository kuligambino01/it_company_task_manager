from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from task.models import Position, Task, TaskType


class SeedDemoDataCommandTests(TestCase):
    def test_command_creates_demo_data(self):
        call_command("seed_demo_data")

        self.assertEqual(Position.objects.count(), 4)
        self.assertEqual(TaskType.objects.count(), 4)
        self.assertEqual(get_user_model().objects.count(), 4)
        self.assertEqual(
            Task.objects.filter(name__startswith="[DEMO]").count(),
            6,
        )

        developer = get_user_model().objects.get(username="developer")

        self.assertTrue(developer.check_password("demo1234"))
        self.assertEqual(developer.position.name, "Developer")

    def test_command_can_be_run_multiple_times_without_duplicates(self):
        call_command("seed_demo_data")
        call_command("seed_demo_data")

        self.assertEqual(Position.objects.count(), 4)
        self.assertEqual(TaskType.objects.count(), 4)
        self.assertEqual(get_user_model().objects.count(), 4)
        self.assertEqual(
            Task.objects.filter(name__startswith="[DEMO]").count(),
            6,
        )
