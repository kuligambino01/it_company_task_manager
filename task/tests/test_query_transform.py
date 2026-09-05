from django.test import RequestFactory, SimpleTestCase

from task.templatetags.query_transform import query_transform


class QueryTransformTests(SimpleTestCase):
    def test_updates_existing_query_parameter(self):
        rf = RequestFactory()
        request = rf.get("/?page=1&status=open")

        result = query_transform(request, page=2)

        self.assertEqual(result, "page=2&status=open")

    def test_adds_new_query_parameter(self):
        rf = RequestFactory()
        request = rf.get("/?page=1")

        result = query_transform(request, status="completed")

        self.assertEqual(result, "page=1&status=completed")

    def test_deletes_query_param(self):
        rf = RequestFactory()
        request = rf.get("/?page=2&status=open")

        result = query_transform(request, page=None)

        self.assertEqual(result, "status=open")

    def test_deletes_non_existing_query_param(self):
        rf = RequestFactory()
        request = rf.get("/?status=open")

        result = query_transform(request, page=None)

        self.assertEqual(result, "status=open")
