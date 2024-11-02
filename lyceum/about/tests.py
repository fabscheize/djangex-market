from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class AboutHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_response(self):
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
