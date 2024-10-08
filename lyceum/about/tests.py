from http import HTTPStatus

from django.test import Client, TestCase


class AboutHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
