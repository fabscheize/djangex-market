from http import HTTPStatus

from django.test import Client, TestCase
from parametrize import parametrize


class HomeHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    @parametrize(
        'path, expected_content, status',
        [
            ('', 'Главная', HTTPStatus.OK),
            ('coffee/', 'Я чайник', HTTPStatus.IM_A_TEAPOT),
        ],
    )
    def test_homepage_response(self, path, expected_content, status):
        response = self.client.get('/' + path)
        self.assertEqual(response.status_code, status)
        self.assertIn(expected_content.encode('utf-8'), response.content)
