from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Item
from core.tests import ContextTest

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


class HomepageContextTest(ContextTest):
    @classmethod
    def setUpTestData(cls):
        cls.response = Client().get(reverse('homepage:home'))

    def test_homepage_correct_context(self):
        self.assertIn('items', type(self).response.context)
        items = type(self).response.context['items']
        for item in items:
            self.assertTrue(hasattr(item, 'tags'))

    def test_homepage_correct_types(self):
        items = type(self).response.context['items']
        for item in items:
            self.assertIsInstance(item, Item)

    def test_homepage_number_of_items(self):
        items = type(self).response.context['items']
        self.assertEqual(len(items), 2)

    def test_homepage_loaded_fields(self):
        items = type(self).response.context['items'][0]
        tags = items.tags.all()[0]

        self.check_instanse_fields(
            items,
            loaded=(
                'name',
                'text',
                'category_id',
            ),
            prefetched=('tags',),
            not_loaded=(
                'is_on_main',
                'is_published',
                'images',
            ),
        )

        self.check_instanse_fields(
            tags,
            loaded=('name',),
            prefetched=(),
            not_loaded=('is_published',),
        )
