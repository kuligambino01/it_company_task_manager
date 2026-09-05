from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from task.tests.base import BaseTaskTestCase


class MyTasksListViewTests(BaseTaskTestCase):
    def setUp(self):
        self.url = reverse("task:my-tasks")

    def test_authenticated_user_gets_200(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_redirects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_uses_my_tasks_list_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response, "task/my_tasks.html")

    def test_task_list_paginates_first_page(self):
        self.client.force_login(self.user)

        for i in range(15):
            task = self.create_task(f"task {i}")
            task.assignees.add(self.user)

        response = self.client.get(self.url)
        page_obj = response.context["page_obj"]
        paginator = response.context["paginator"]

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 10)
        self.assertEqual(page_obj.number, 1)
        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(paginator.count, 15)

    def test_task_list_paginates_second_page(self):
        self.client.force_login(self.user)

        for i in range(15):
            task = self.create_task(f"task {i}")
            task.assignees.add(self.user)

        response = self.client.get(self.url, {"page": 2})
        page_obj = response.context["page_obj"]
        paginator = response.context["paginator"]

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(page_obj.number, 2)
        self.assertFalse(page_obj.has_next())
        self.assertTrue(page_obj.has_previous())
        self.assertEqual(paginator.count, 15)
        self.assertEqual(len(response.context["task_list"]), 5)

    def test_displays_only_current_user_tasks(self):
        self.client.force_login(self.user)
        user_2 = get_user_model().objects.create_user(username="test123",
                                                      password="test123",
                                                      position=self.position)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_3 = self.create_task("task 3", is_completed=False)
        task_4 = self.create_task("task 4")

        task_4.assignees.add(self.user)
        task_2.assignees.add(self.user)
        task_1.assignees.add(self.user)
        task_3.assignees.add(user_2)

        response = self.client.get(self.url)

        self.assertCountEqual(
            list(response.context["task_list"]), [task_1, task_2, task_4], )

    def test_displays_task_assigned_to_multiple_users(self):
        self.client.force_login(self.user)
        user_2 = get_user_model().objects.create_user(username="test123",
                                                      password="test123",
                                                      position=self.position)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_4 = self.create_task("task 4")

        task_4.assignees.add(self.user, user_2)
        task_2.assignees.add(self.user, user_2)
        task_1.assignees.add(self.user, user_2)

        response = self.client.get(self.url)

        self.assertCountEqual(
            list(response.context["task_list"]), [task_1, task_2, task_4], )

    def test_filters_open_tasks(self):
        self.client.force_login(self.user)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_3 = self.create_task("task 3", is_completed=False)
        task_4 = self.create_task("task 4", is_completed=False)

        task_4.assignees.add(self.user)
        task_2.assignees.add(self.user)
        task_1.assignees.add(self.user)
        task_3.assignees.add(self.user)

        response = self.client.get(self.url, {"status": "open"})

        self.assertCountEqual(
            list(response.context["task_list"]), [task_3, task_2, task_4], )

    def test_filters_completed_tasks(self):
        self.client.force_login(self.user)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_3 = self.create_task("task 3", is_completed=False)
        task_4 = self.create_task("task 4", is_completed=False)

        task_4.assignees.add(self.user)
        task_2.assignees.add(self.user)
        task_1.assignees.add(self.user)
        task_3.assignees.add(self.user)

        response = self.client.get(self.url, {"status": "completed"})

        self.assertCountEqual(
            list(response.context["task_list"]), [task_1])

    def test_without_status_displays_all_user_tasks(self):
        self.client.force_login(self.user)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_3 = self.create_task("task 3", is_completed=False)
        task_4 = self.create_task("task 4", is_completed=False)

        task_4.assignees.add(self.user)
        task_2.assignees.add(self.user)
        task_1.assignees.add(self.user)
        task_3.assignees.add(self.user)

        response = self.client.get(self.url)

        self.assertCountEqual(
            list(response.context["task_list"]), [task_1, task_3, task_2, task_4])

    def test_invalid_status_displays_all_user_tasks(self):
        self.client.force_login(self.user)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_3 = self.create_task("task 3", is_completed=False)
        task_4 = self.create_task("task 4", is_completed=False)

        task_4.assignees.add(self.user)
        task_2.assignees.add(self.user)
        task_1.assignees.add(self.user)
        task_3.assignees.add(self.user)

        response = self.client.get(self.url, {"status": "abc"})

        self.assertCountEqual(
            list(response.context["task_list"]), [task_1, task_3, task_2, task_4])

    def test_tasks_are_ordered_by_deadline(self):
        self.client.force_login(self.user)

        now = timezone.now()

        task_1 = self.create_task(
            "task 1",
            deadline=now + timedelta(days=4),
        )
        task_2 = self.create_task(
            "task 2",
            deadline=now + timedelta(days=2),
        )
        task_3 = self.create_task(
            "task 3",
            deadline=now + timedelta(days=3),
        )
        task_3.assignees.add(self.user)
        task_2.assignees.add(self.user)
        task_1.assignees.add(self.user)

        response = self.client.get(self.url)

        task_list = list(response.context["task_list"])

        self.assertEqual(task_list, [task_2, task_3, task_1])

