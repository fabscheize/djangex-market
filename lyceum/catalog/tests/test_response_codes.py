from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from parametrize import parametrize

__all__ = []


class CatalogHttpResponseTest(TestCase):
    fixtures = ['data.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    @parametrize(
        'path, args',
        [
            ('item', ['1']),
            ('item', ['0001']),
            ('new', None),
            ('friday', None),
            ('unverified', None),
        ],
    )
    def test_catalog_response_positive(self, path, args):
        response = self.client.get(reverse('catalog:' + path, args=args))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parametrize(
        'path, pk',
        [
            ('item', '2'),
        ],
    )
    def test_catalog_response_negative(self, path, pk):
        response = self.client.get(reverse('catalog:' + path, args=[pk]))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
