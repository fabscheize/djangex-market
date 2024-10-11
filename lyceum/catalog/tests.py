from http import HTTPStatus
from random import randint

from django.test import Client, TestCase


class CatalogHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_catalog_status_code(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_item_from_catalog_status_code(self):
        pk = randint(0, 100)
        response = self.client.get(f'/catalog/{pk}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_re_item_from_catalog_status_code(self):
        pk = randint(1, 100)
        response = self.client.get(f'/catalog/re/{pk}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(f'{pk}'.encode('utf-8'), response.content)

        pk = -1
        response = self.client.get(f'/catalog/re/{pk}/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get('/catalog/re/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get('/catalog/re/qwerty/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_converter_item_from_catalog_status_code(self):
        pk = randint(1, 100)
        response = self.client.get(f'/catalog/converter/{pk}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(f'{pk}'.encode('utf-8'), response.content)

        pk = -1
        response = self.client.get(f'/catalog/converter/{pk}/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get('/catalog/converter/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get('/catalog/converter/qwerty/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
