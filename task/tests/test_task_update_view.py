from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from task.forms import TaskForm
from task.models import Task
from task.tests.base import BaseTaskTestCase


class TaskUpdateViewTests(BaseTaskTestCase):
    def setUp(self):
        self.task = self.create_task(name="test")

        self.url = reverse("task:task-update", kwargs={"pk": self.task.pk})

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

    def test_task_update_returns_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        form = response.context["form"]

        self.assertIsInstance(form, TaskForm)
        self.assertEqual(form.instance, self.task)

    def test_valid_post_updates_task(self):
        self.client.force_login(self.user)

        now = timezone.now() + timedelta(days=5)
        deadline = now.strftime("%Y-%m-%dT%H:%M")

        self.assertEqual(Task.objects.count(), 1)

        response = self.client.post(self.url,
                                    {
                                        "name": "test123",
                                        "description": "321test",
                                        "deadline": deadline,
                                        "priority": "high",
                                        "task_type": self.task_type.pk,
                                        "assignees": [self.user.pk]
                                    })

        self.task.refresh_from_db()

        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(self.task.name, "test123")
        self.assertEqual(self.task.description, "321test")
        self.assertEqual(self.task.priority, "high")
        self.assertEqual(self.task.task_type, self.task_type)
        self.assertIn(self.user, self.task.assignees.all())

        self.assertRedirects(response, reverse("task:task-detail", kwargs={"pk": self.task.pk}))

    def test_task_update_with_deadline_in_past(self):
        self.client.force_login(self.user)

        now = timezone.now() - timedelta(days=1)
        deadline = now.strftime("%Y-%m-%dT%H:%M")

        self.assertEqual(Task.objects.count(), 1)

        response = self.client.post(self.url,
                                    {"name": "test1",
                                     "description": "test123",
                                     "deadline": deadline,
                                     "priority": "low",
                                     "task_type": self.task_type.pk,
                                     "assignees": [self.user.pk]
                                     })
        self.task.refresh_from_db()

        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 1)
        self.assertIn("deadline", form.errors)

    def test_update_allows_unchanged_expired_deadline(self):
        self.client.force_login(self.user)

        expired_deadline = (
                timezone.now() - timedelta(days=1)
        ).replace(second=0, microsecond=0)

        self.task.deadline = expired_deadline
        self.task.assignees.add(self.user)
        self.task.save(update_fields=["deadline"])

        response = self.client.post(
            self.url, {
                "name": self.task.name,
                "description": "Updated description",
                "deadline": expired_deadline.strftime("%Y-%m-%dT%H:%M"),
                "priority": self.task.priority,
                "task_type": self.task.task_type.pk,
                "assignees": [self.user.pk]})

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.description, "Updated description")
        self.assertEqual(self.task.deadline, expired_deadline)
        self.assertEqual(Task.objects.count(), 1)

    def test_nonexistent_task_returns_404(self):
        self.client.force_login(self.user)

        url = reverse("task:task-update", kwargs={"pk": 9999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)