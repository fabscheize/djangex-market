from random import randint

from django.test import Client, TestCase


class CatalogHttpResponseTest(TestCase):
    def test_catalog_status_code(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_item_from_catalog_status_code(self):
        id = randint(0, 100)
        response = Client().get(f'/catalog/{id}/')
        self.assertEqual(response.status_code, 200)

    def test_re_item_from_catalog_status_code(self):
        id = randint(1, 100)
        response = Client().get(f'/catalog/re/{id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'{id}'.encode('utf-8'), response.content)
        id = -1
        response = Client().get(f'/catalog/re/{id}/')
        self.assertEqual(response.status_code, 404)
        response = Client().get('/catalog/re/')
        self.assertEqual(response.status_code, 404)
        response = Client().get('/catalog/re/qerty/')
        self.assertEqual(response.status_code, 404)

    def test_converter_item_from_catalog_status_code(self):
        id = randint(1, 100)
        response = Client().get(f'/catalog/converter/{id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'{id}'.encode('utf-8'), response.content)
        id = -1
        response = Client().get(f'/catalog/converter/{id}/')
        self.assertEqual(response.status_code, 404)
        response = Client().get('/catalog/converter/')
        self.assertEqual(response.status_code, 404)
        response = Client().get('/catalog/converter/qerty/')
        self.assertEqual(response.status_code, 404)
