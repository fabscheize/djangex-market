from http import HTTPStatus

from django.test import Client, TestCase


class HomeHttpResponseTest(TestCase):
    def test_homepage_status_code(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_coffee_status_code(self):
        response = Client().get('/coffee/')
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertIn('Я чайник'.encode('utf-8'), response.content)
