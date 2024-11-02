from django.core.exceptions import ValidationError
from django.test import TestCase
from parametrize import parametrize

from catalog.models import Category, Tag

__all__ = []


def create_and_save_entry(model_class, **kwargs):
    instance = model_class(**kwargs)
    instance.full_clean()
    instance.save()


class NormalizedNameTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='Категория 1',
            slug='category-1',
            weight=100,
        )
        cls.tag = Tag.objects.create(
            name='Тег 1',
            slug='tag-1',
        )

    @parametrize(
        'name',
        [
            ('Категория_1'),
            ('Категория 1!'),
            ('категория 1'),
            ('Kатегория 1'),
        ],
    )
    def test_category_normalized_name(self, name):
        element_count = Category.objects.count()

        with self.assertRaises(ValidationError):
            create_and_save_entry(
                Category,
                name=name,
                slug='category-2',
                weight=100,
            )

        self.assertEqual(Category.objects.count(), element_count)

    @parametrize(
        'name',
        [
            ('Тег_1'),
            ('Тег 1!'),
            ('тег 1'),
            ('Tег 1'),
        ],
    )
    def test_tag_normalized_name(self, name):
        element_count = Tag.objects.count()

        with self.assertRaises(ValidationError):
            create_and_save_entry(
                Tag,
                name=name,
                slug='tag-2',
            )

        self.assertEqual(Tag.objects.count(), element_count)
