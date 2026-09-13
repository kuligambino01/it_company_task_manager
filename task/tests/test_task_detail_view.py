from django.urls import reverse

from task.tests.base import BaseTaskTestCase


class TaskDetailViewTests(BaseTaskTestCase):
    def setUp(self):
        self.task = self.create_task(name="test")

        self.url = reverse("task:task-detail", kwargs={"pk": self.task.pk})

    def test_authenticated_user_gets_200(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_redirects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_view_uses_task_detail_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "task/task_detail.html")

    def test_displays_correct_task(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        task_details = response.context["object"]

        self.assertEqual(task_details, self.task)

    def test_nonexistent_task_returns_404(self):
        self.client.force_login(self.user)

        url = reverse("task:task-detail", kwargs={"pk": 555})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
