from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from parametrize import parametrize

__all__ = []


class AboutHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    @parametrize(
        'status',
        [
            (HTTPStatus.OK),
        ],
    )
    def test_homepage_response(self, status):
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.status_code, status)
