from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from task.tests.base import BaseTaskTestCase


class TaskListViewTests(BaseTaskTestCase):
    def setUp(self):
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

        self.assertTemplateUsed(
            response, "task/task_list.html")

    def test_task_list_paginates_first_page(self):
        self.client.force_login(self.user)

        for i in range(15):
            self.create_task(f"task {i}")

        response = self.client.get(self.url)
        page_obj = response.context["page_obj"]
        paginator = response.context["paginator"]

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 10)
        self.assertEqual(page_obj.number, 1)
        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.object_list), 15)

    def test_task_list_paginates_second_page(self):
        self.client.force_login(self.user)

        for i in range(15):
            self.create_task(f"task {i}")

        response = self.client.get(self.url, {"page": 2})
        page_obj = response.context["page_obj"]
        paginator = response.context["paginator"]

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(page_obj.number, 2)
        self.assertFalse(page_obj.has_next())
        self.assertTrue(page_obj.has_previous())
        self.assertEqual(len(paginator.object_list), 15)
        self.assertEqual(len(response.context["task_list"]), 5)

    def test_task_list_is_ordered_by_deadline(self):
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

        response = self.client.get(self.url)

        task_list = list(response.context["task_list"])

        self.assertEqual(task_list, [task_2, task_3, task_1])

    def test_search_by_query_param_true(self):
        self.client.force_login(self.user)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_3 = self.create_task("task 3", is_completed=False)

        response = self.client.get(self.url, {"is_completed": "true"})

        tasks = response.context["task_list"]

        self.assertCountEqual(tasks, [task_1])

    def test_search_by_query_param_false(self):
        self.client.force_login(self.user)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_3 = self.create_task("task 3", is_completed=False)

        response = self.client.get(self.url, {"is_completed": "false"})

        tasks = response.context["task_list"]

        self.assertCountEqual(tasks, [task_2, task_3])

    def test_search_without_query_param(self):
        self.client.force_login(self.user)

        task_1 = self.create_task("task 1")
        task_2 = self.create_task("task 2")
        task_3 = self.create_task("task 3")
        task_4 = self.create_task("task 4")

        response = self.client.get(self.url)

        self.assertCountEqual(
            list(response.context["task_list"]), [task_1, task_2, task_3, task_4])

    def test_search_with_invalid_query_param(self):
        self.client.force_login(self.user)

        task_2 = self.create_task("task 2", is_completed=False)
        task_1 = self.create_task("task 1", is_completed=True)
        task_3 = self.create_task("task 3", is_completed=False)

        response = self.client.get(self.url, {"is_completed": "abc"})

        tasks = response.context["task_list"]

        self.assertCountEqual(tasks, [task_2, task_1, task_3])

    def test_exactly_ten_tasks_are_not_paginated(self):
        self.client.force_login(self.user)

        for i in range(10):
            self.create_task(f"task {i}")

        response = self.client.get(self.url)
        page_obj = response.context["page_obj"]
        paginator = response.context["paginator"]

        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 10)
        self.assertEqual(page_obj.number, 1)
        self.assertFalse(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())
        self.assertEqual(paginator.num_pages, 1)
