from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task.models import Task, TaskType, Position, Priority


class DashboardViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Bug")

        self.url = reverse("task:dashboard")

    def create_task(self, name, **kwargs):
        return Task.objects.create(
            name=name,
            description="Test description",
            deadline=timezone.now() + timedelta(days=1),
            priority=Priority.MEDIUM,
            task_type=self.task_type,
            **kwargs,
        )

    def test_authenticated_user_gets_200(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_redirects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_correct_task_count(self):
        self.client.force_login(self.user)

        self.create_task("task 1")
        self.create_task("task 2")
        self.create_task("task 3")

        response = self.client.get(self.url)

        self.assertEqual(response.context["tasks"], 3)

    def test_correct_completed_tasks_count(self):
        self.client.force_login(self.user)

        self.create_task("task", is_completed=True)
        self.create_task("task 2", is_completed=True)
        self.create_task("task 3")
        self.create_task("task 4")

        response = self.client.get(self.url)

        self.assertEqual(response.context["completed_tasks"], 2)

    def test_correct_open_tasks_count(self):
        self.client.force_login(self.user)

        self.create_task("task", is_completed=True)
        self.create_task("task 2", is_completed=True)
        self.create_task("task 3")
        self.create_task("task 4")
        self.create_task("task 5")

        response = self.client.get(self.url)

        self.assertEqual(response.context["open_tasks"], 3)

    def test_my_tasks_are_limited_to_five(self):
        self.client.force_login(self.user)

        for i in range(10):
            task = self.create_task(f"test {i}", is_completed=False)
            task.assignees.add(self.user)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["my_tasks"]), 5)

    def test_correct_worker_count(self):
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="test2",
            password="test123",
            position=self.position,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.context["workers"], 2)

    def test_my_tasks_contains_only_current_user_open_tasks(self):
        self.client.force_login(self.user)
        user_2 = get_user_model().objects.create_user(
            username="test2",
            password="test123",
            position=self.position,
        )
        own_open_tasks = []

        for i in range(5):
            task = self.create_task(f"test {i}", is_completed=False)
            task.assignees.add(user_2)

        for i in range(3):
            task = self.create_task(f"test {i}", is_completed=True)
            task.assignees.add(self.user)

        for i in range(4):
            task = self.create_task(f"test {i}", is_completed=False)
            task.assignees.add(self.user)
            own_open_tasks.append(task)

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["my_tasks"]), 4)
        self.assertCountEqual(list(response.context["my_tasks"]), own_open_tasks)

    def test_my_tasks_are_ordered_by_deadline(self):
        self.client.force_login(self.user)

        task_1 = Task.objects.create(
            name="test",
            description="Test description",
            deadline=timezone.now() + timedelta(days=4),
            priority=Priority.MEDIUM,
            task_type=self.task_type,
        )
        task_2 = Task.objects.create(
            name="test",
            description="Test description",
            deadline=timezone.now() + timedelta(days=2),
            priority=Priority.MEDIUM,
            task_type=self.task_type,
        )
        task_3 = Task.objects.create(
            name="test",
            description="Test description",
            deadline=timezone.now() + timedelta(days=3),
            priority=Priority.MEDIUM,
            task_type=self.task_type,
        )

        task_1.assignees.add(self.user)
        task_2.assignees.add(self.user)
        task_3.assignees.add(self.user)

        response = self.client.get(self.url)
        my_tasks = list(response.context["my_tasks"])

        self.assertEqual(my_tasks, [task_2, task_3, task_1])

    def test_uses_dashboard_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "task/dashboard.html")

    def test_dashboard_with_no_tasks(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.context["tasks"], 0)
        self.assertEqual(response.context["completed_tasks"], 0)
        self.assertEqual(response.context["open_tasks"], 0)
        self.assertEqual(list(response.context["my_tasks"]), [])


class TaskListViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Bug")

        self.url = reverse("task:task-list")

    def test_authenticated_user_gets_200(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_redirects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_uses_task_list_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "task/task_list.html")

    def test_task_list_display(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        tasks = response.context["task_list"]


