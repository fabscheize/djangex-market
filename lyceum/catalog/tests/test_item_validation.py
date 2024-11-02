from django.core.exceptions import ValidationError
from django.test import TestCase
from parametrize import parametrize

from catalog.models import Category, Item

__all__ = []


def create_and_save_entry(model_class, **kwargs):
    instance = model_class(**kwargs)
    instance.full_clean()
    instance.save()


class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='Категория',
            slug='category',
            weight=100,
        )

    @parametrize(
        'name, text',
        [
            ('Товар 1', 'Это превосходно оформленный товар.'),
            ('Товар 2', 'Роскошно иметь такой товар.'),
            ('A' * 150, 'Это превосходно оформленный товар.'),
        ],
    )
    def test_item_validation_positive(self, name, text):
        element_count = Item.objects.count()

        create_and_save_entry(
            Item,
            name=name,
            text=text,
            category=ItemModelTest.category,
        )

        self.assertEqual(
            Item.objects.count(),
            element_count + 1,
        )

    @parametrize(
        'name, text',
        [
            ('A' * 151, 'Это превосходно оформленный товар.'),
            ('Товар 3', 'Отстойный товар без нужных слов.'),
            ('Товар 3', 'Ппревосходно превосх0дно роскошно0'),
        ],
    )
    def test_item_validation_negative(self, name, text):
        element_count = Item.objects.count()

        with self.assertRaises(ValidationError):
            create_and_save_entry(
                Item,
                name=name,
                text=text,
                category=ItemModelTest.category,
            )

        self.assertEqual(
            Item.objects.count(),
            element_count,
        )
