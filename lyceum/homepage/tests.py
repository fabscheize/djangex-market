from http import HTTPStatus

from django.test import Client, override_settings, TestCase
from django.urls import reverse

from catalog.models import Item, Tag
from users.models import User

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


class HomepageHttpResponseTest(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get(reverse('homepage:home'))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            msg='Could not reach the endpoint',
        )

    @override_settings(ALLOW_REVERSE=False, DEFAULT_USER_ACTIVITY=True)
    def test_coffee_status_code(self):
        user = User.objects.create(username='testuser')
        user.set_password('AA385W3ersHHGv')
        user.save()
        self.client.login(username='testuser', password='AA385W3ersHHGv')
        response = self.client.get(reverse('homepage:coffee'))

        self.assertEqual(
            response.status_code,
            HTTPStatus.IM_A_TEAPOT,
            msg='Could not reach the endpoint',
        )
        self.assertIn(
            'Я чайник'.encode('utf-8'),
            response.content,
            msg='"Я чайник" is not the content',
        )


class HomepageContextTest(ContextTest):
    @classmethod
    def setUpTestData(cls):
        cls.response = Client().get(reverse('homepage:home'))

    def test_homepage_correct_context(self):
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

    def test_homepage_correct_types(self):
        items = type(self).response.context['items']
        for item in items:
            self.assertIsInstance(
                item,
                Item,
                msg='Item attribute is not Item model',
            )

    def test_homepage_number_of_items(self):
        items = type(self).response.context['items']
        self.assertEqual(
            len(items),
            2,
            msg='The number of objects does not match '
            'the number in the fixtures',
        )

    def test_homepage_loaded_fields(self):
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
            not_loaded=(
                Item.is_published.field.name,
                Item.is_on_main.field.name,
            ),
        )

        self.check_instanse_fields(
            tags,
            loaded=(Tag.name.field.name,),
            prefetched=(),
            not_loaded=(Tag.is_published.field.name,),
        )
