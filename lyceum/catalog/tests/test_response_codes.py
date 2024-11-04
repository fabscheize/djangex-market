from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from parametrize import parametrize

from catalog.models import Category, Item


__all__ = []


class CatalogHttpResponseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.category = Category.objects.create(
            name='Категория',
            slug='category',
            weight=100,
        )
        cls.item = Item.objects.create(
            name='Товар 1',
            text='Превосходно тестируем код',
            category=cls.category,
        )

    @parametrize(
        'path, pk',
        [
            ('item', '1'),
            ('item', '0001'),
        ],
    )
    def test_catalog_response_positive(self, path, pk):
        response = self.client.get(reverse('catalog:' + path, args=[pk]))
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
