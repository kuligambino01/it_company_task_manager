from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from task.forms import TaskForm
from task.models import Task
from task.tests.base import BaseTaskTestCase


class TaskCreateViewTests(BaseTaskTestCase):
    def setUp(self):
        self.url = reverse("task:task-create")

    def test_authenticated_user_gets_200(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_redirects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_uses_task_form_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response, "task/task_form.html")

    def test_task_create_returns_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        form = response.context["form"]

        self.assertIsInstance(form, TaskForm)

    def test_valid_post_creates_task(self):
        self.client.force_login(self.user)

        now = timezone.now() + timedelta(days=1)
        deadline = now.strftime("%Y-%m-%dT%H:%M")

        self.assertEqual(Task.objects.count(), 0)

        response = self.client.post(self.url,
                                    {"name": "test1",
                                     "description": "test123",
                                     "deadline": deadline,
                                     "priority": "low",
                                     "task_type": self.task_type.pk,
                                     "assignees": [self.user.pk]
                                     })

        task = Task.objects.get(name="test1")

        self.assertEqual(task.name, "test1")
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.description, "test123")
        self.assertEqual(task.priority, "low")
        self.assertEqual(task.task_type, self.task_type)

        self.assertIn(self.user, task.assignees.all())

        self.assertRedirects(response, reverse("task:task-list"))

    def test_task_create_with_deadline_in_past(self):
        self.client.force_login(self.user)

        now = timezone.now() - timedelta(days=1)
        deadline = now.strftime("%Y-%m-%dT%H:%M")

        self.assertEqual(Task.objects.count(), 0)

        response = self.client.post(self.url,
                                    {"name": "test1",
                                     "description": "test123",
                                     "deadline": deadline,
                                     "priority": "low",
                                     "task_type": self.task_type.pk,
                                     "assignees": [self.user.pk]
                                     })
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)
        self.assertIn("deadline", form.errors)
