from django.test import TestCase, Client


class HomeHttpResponseTest(TestCase):
    def test_homepage_status_code(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)
