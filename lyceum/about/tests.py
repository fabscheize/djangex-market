from http import HTTPStatus

from django.test import Client, TestCase
from parametrize import parametrize


class AboutHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    @parametrize(
        'path, expected_content, status',
        [
            ('', 'О проекте', HTTPStatus.OK),
        ],
    )
    def test_homepage_response(self, path, expected_content, status):
        response = self.client.get('/about/' + path)
        self.assertEqual(response.status_code, status)
        self.assertIn(expected_content.encode('utf-8'), response.content)
