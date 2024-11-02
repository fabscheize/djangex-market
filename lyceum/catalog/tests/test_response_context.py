from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Category, Item, Tag

__all__ = []


class CatalogListContextTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.published_category = Category.objects.create(
            name='Опубликованная категория',
            slug='published_category',
            weight=100,
        )

        cls.published_tag = Tag.objects.create(
            name='Опубликованный тег',
            slug='published_tag',
        )

        cls.unpublished_tag = Tag.objects.create(
            name='Неопубликованный тег',
            slug='unpublished_tag',
            is_published=False,
        )

        cls.published_item = Item.objects.create(
            name='Опубликованный товар',
            text='Превосходно тестируем код',
            category=cls.published_category,
        )
        cls.published_item.tags.add(cls.published_tag)
        cls.published_item.tags.add(cls.unpublished_tag)

        cls.unpublished_item = Item.objects.create(
            name='Неопубликованный товар',
            text='Превосходно тестируем код',
            category=cls.published_category,
            is_published=False,
        )

        cls.response = Client().get(reverse('catalog:list'))

    def test_catalog_correct_context(self):
        self.assertIn('items', CatalogListContextTest.response.context)
        items = CatalogListContextTest.response.context['items']
        for item in items:
            self.assertTrue(hasattr(item, 'tags'))

    def test_catalog_number_of_items(self):
        items = CatalogListContextTest.response.context['items']
        self.assertEqual(items.count(), 1)

    def test_catalog_number_of_tags(self):
        items = CatalogListContextTest.response.context['items']
        for item in items:
            tags = item.tags.all()
            self.assertEqual(tags.count(), 1)
