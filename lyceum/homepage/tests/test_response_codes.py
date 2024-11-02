from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class HomepageHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_status_code(self):
        response = self.client.get(reverse('homepage:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_status_code(self):
        response = self.client.get(reverse('homepage:coffee'))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual('Я чайник'.encode('utf-8'), response.content)
