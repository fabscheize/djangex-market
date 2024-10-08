from random import randint

from django.test import Client, TestCase


class CatalogHttpResponseTest(TestCase):
    def test_catalog_status_code(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_item_from_catalog_status_code(self):
        id = randint(1, 100)
        response = Client().get(f'/catalog/{id}')
        self.assertEqual(response.status_code, 200)
