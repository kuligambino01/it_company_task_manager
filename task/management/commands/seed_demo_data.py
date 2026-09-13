from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from task.models import Position, Priority, Task, TaskType


class Command(BaseCommand):
    help = "Create demo data for the task manager"

    def handle(self, *args, **options):
        positions = {
            name: Position.objects.get_or_create(name=name)[0]
            for name in (
                "Developer",
                "Designer",
                "Project Manager",
                "QA",
            )
        }

        task_types = {
            name: TaskType.objects.get_or_create(name=name)[0]
            for name in (
                "Bug",
                "Feature",
                "Improvement",
                "Testing",
            )
        }

        users_data = [
            ("developer", "Developer"),
            ("designer", "Designer"),
            ("manager", "Project Manager"),
            ("qa", "QA"),
        ]

        users = {}

        for username, position_name in users_data:
            user, _ = get_user_model().objects.get_or_create(
                username=username,
                defaults={
                    "position": positions[position_name],
                },
            )

            user.position = positions[position_name]
            user.set_password("demo1234")
            user.save()

            users[username] = user

        Task.objects.filter(name__startswith="[DEMO]").delete()

        now = timezone.now()

        tasks_data = [
            {
                "name": "[DEMO] Fix login validation",
                "description": "Fix validation errors on the login page.",
                "deadline": now + timedelta(days=1),
                "priority": Priority.URGENT,
                "task_type": task_types["Bug"],
                "is_completed": False,
                "assignees": [users["developer"], users["qa"]],
            },
            {
                "name": "[DEMO] Create dashboard design",
                "description": "Prepare the new dashboard interface.",
                "deadline": now + timedelta(days=3),
                "priority": Priority.HIGH,
                "task_type": task_types["Feature"],
                "is_completed": False,
                "assignees": [users["designer"]],
            },
            {
                "name": "[DEMO] Improve task filtering",
                "description": "Add improvements to task filtering.",
                "deadline": now + timedelta(days=5),
                "priority": Priority.MEDIUM,
                "task_type": task_types["Improvement"],
                "is_completed": False,
                "assignees": [users["developer"]],
            },
            {
                "name": "[DEMO] Test task assignment",
                "description": "Verify assigning and unassigning workers.",
                "deadline": now + timedelta(days=2),
                "priority": Priority.HIGH,
                "task_type": task_types["Testing"],
                "is_completed": True,
                "assignees": [users["qa"]],
            },
            {
                "name": "[DEMO] Prepare sprint tasks",
                "description": "Prepare tasks for the next development sprint.",
                "deadline": now + timedelta(days=7),
                "priority": Priority.MEDIUM,
                "task_type": task_types["Feature"],
                "is_completed": False,
                "assignees": [
                    users["manager"],
                    users["developer"],
                ],
            },
            {
                "name": "[DEMO] Review completed feature",
                "description": "Review the recently completed feature.",
                "deadline": now - timedelta(days=1),
                "priority": Priority.LOW,
                "task_type": task_types["Testing"],
                "is_completed": True,
                "assignees": [
                    users["manager"],
                    users["qa"],
                ],
            },
        ]

        for task_data in tasks_data:
            assignees = task_data.pop("assignees")

            task = Task.objects.create(**task_data)
            task.assignees.set(assignees)

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
