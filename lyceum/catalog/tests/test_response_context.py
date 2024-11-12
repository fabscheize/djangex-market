from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Item, Tag

__all__ = []


class ContextTest(TestCase):
    fixtures = ['data.json']

    def check_instanse_fields(self, instance, loaded, prefetched, not_loaded):
        instance_dict = instance.__dict__

        for field in loaded:
            self.assertIn(
                field,
                instance_dict,
                msg='There are no required fields in context',
            )

        for field in prefetched:
            self.assertIn(
                field,
                instance_dict['_prefetched_objects_cache'],
                msg='There are no required prefetched fields in context',
            )

        for field in not_loaded:
            self.assertNotIn(
                field,
                instance_dict,
                msg='There are some unnecessary fields in context',
            )


class CatalogContextTest(ContextTest):
    @classmethod
    def setUpTestData(cls):
        cls.response = Client().get(reverse('catalog:list'))

    def test_catalog_correct_context(self):
        self.assertIn(
            'items',
            type(self).response.context,
            msg='There are no items in context',
        )
        items = type(self).response.context['items']
        for item in items:
            self.assertTrue(
                hasattr(item, 'tags'),
                msg='There are no tags in context',
            )

    def test_catalog_correct_types(self):
        items = type(self).response.context['items']
        for item in items:
            self.assertIsInstance(
                item,
                Item,
                msg='Item attribute is not Item model',
            )

    def test_catalog_number_of_items(self):
        items = type(self).response.context['items']
        self.assertEqual(len(items), 5)

    def test_catalog_loaded_fields(self):
        items = type(self).response.context['items'][0]
        tags = items.tags.all()[0]

        self.check_instanse_fields(
            items,
            loaded=(
                Item.name.field.name,
                Item.text.field.name,
                Item.category.field.column,
            ),
            prefetched=(Item.tags.field.name,),
            not_loaded=(Item.is_published.field.name,),
        )

        self.check_instanse_fields(
            tags,
            loaded=(Tag.name.field.name,),
            prefetched=(),
            not_loaded=(Tag.is_published.field.name,),
        )
