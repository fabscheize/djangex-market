from django.core.exceptions import ValidationError
from django.test import TestCase
from parametrize import parametrize

from catalog.models import Category

__all__ = []


def create_and_save_entry(model_class, **kwargs):
    instance = model_class(**kwargs)
    instance.full_clean()
    instance.save()


class CategoryModelTest(TestCase):
    @parametrize(
        'name, slug, weight',
        [
            ('Категория 1', 'category-1', 100),
            ('А' * 150, 'category-1', 100),
            ('Категория 2', '_' * 200, 100),
            ('Категория 3', 'category-3', 1),
        ],
    )
    def test_category_validation_positive(self, name, slug, weight):
        element_count = Category.objects.count()

        create_and_save_entry(
            Category,
            name=name,
            slug=slug,
            weight=weight,
        )

        self.assertEqual(
            Category.objects.count(),
            element_count + 1,
        )

    @parametrize(
        'name, slug, weight',
        [
            ('А' * 151, 'category-2', 100),
            ('Категория 2', '_' * 201, 100),
            ('Категория 2', 'невалидный_слаг', 100),
            ('Категория 2', 'invalid slug', 100),
            ('Категория 2', 'invalid_slug!', 100),
            ('Категория 3', 'category-3', 0),
        ],
    )
    def test_category_validation_negative(self, name, slug, weight):
        element_count = Category.objects.count()

        with self.assertRaises(ValidationError):
            create_and_save_entry(
                Category,
                name=name,
                slug=slug,
                weight=weight,
            )

        self.assertEqual(
            Category.objects.count(),
            element_count,
        )
