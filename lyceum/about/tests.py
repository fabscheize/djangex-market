from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from parametrize import parametrize


class AboutHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    @parametrize(
        'expected_content, status',
        [
            ('О проекте', HTTPStatus.OK),
        ],
    )
    def test_homepage_response(self, expected_content, status):
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.status_code, status)
        self.assertIn(expected_content.encode('utf-8'), response.content)
