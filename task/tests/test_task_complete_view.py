from django.urls import reverse

from task.tests.base import BaseTaskTestCase


class TaskCompleteViewTests(BaseTaskTestCase):
    def setUp(self):
        self.task = self.create_task(name="test task",
                                     is_completed=False)

        self.url = reverse("task:task-complete", kwargs={"pk": self.task.pk})

    def test_user_gets_405_using_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)

    def test_anonymous_user_redirects(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_post_marks_task_as_completed(self):
        self.client.force_login(self.user)
        self.assertFalse(self.task.is_completed)

        response = self.client.post(self.url)

        self.task.refresh_from_db()

        self.assertTrue(self.task.is_completed)
        self.assertRedirects(response, reverse("task:task-list"))

    def test_nonexistent_task_returns_404(self):
        self.client.force_login(self.user)

        url = reverse("task:task-complete", kwargs={"pk": 9999})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

