from django.contrib.auth import get_user_model
from django.urls import reverse

from task.tests.base import BaseTaskTestCase


class AssignTaskViewTests(BaseTaskTestCase):
    def setUp(self):
        self.task = self.create_task(name="test task")

        self.url = reverse("task:task-assign", kwargs={"pk": self.task.pk})

    def test_user_gets_405_using_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)

    def test_anonymous_user_redirects(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_post_assigns_user_to_task(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url)

        self.assertIn(self.user, self.task.assignees.all())
        self.assertRedirects(response, reverse("task:task-detail", kwargs={"pk": self.task.pk}))

    def test_post_unassigns_user_from_task(self):
        self.client.force_login(self.user)

        self.task.assignees.add(self.user)

        response = self.client.post(self.url)

        self.assertNotIn(self.user, self.task.assignees.all())
        self.assertRedirects(response, reverse("task:task-detail", kwargs={"pk": self.task.pk}))

    def test_nonexistent_task_returns_404(self):
        self.client.force_login(self.user)

        url = reverse("task:task-assign", kwargs={"pk": 9999})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

    def test_post_assigns_user_without_removing_existing_assignees(self):
        self.client.force_login(self.user)
        user_2 = get_user_model().objects.create_user(username="test123",
                                                      password="test123",
                                                      position=self.position)
        self.task.assignees.add(user_2)

        response = self.client.post(self.url)

        self.assertEqual(self.task.assignees.count(), 2)
        self.assertCountEqual(self.task.assignees.all(), [user_2, self.user])
