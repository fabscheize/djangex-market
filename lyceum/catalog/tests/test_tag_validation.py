from django.core.exceptions import ValidationError
from django.test import TestCase
from parametrize import parametrize

from catalog.models import Tag

__all__ = []


def create_and_save_entry(model_class, **kwargs):
    instance = model_class(**kwargs)
    instance.full_clean()
    instance.save()


class TagModelTest(TestCase):
    @parametrize(
        'name, slug',
        [
            ('Тег 1', 'tag-1'),
            ('А' * 150, 'tag-2'),
            ('Тег 2', '_' * 200),
        ],
    )
    def test_tag_validation_positive(self, name, slug):
        element_count = Tag.objects.count()

        create_and_save_entry(
            Tag,
            name=name,
            slug=slug,
        )

        self.assertEqual(
            Tag.objects.count(),
            element_count + 1,
            msg='New object has not been created',
        )

    @parametrize(
        'name, slug',
        [
            ('А' * 151, 'tag-2'),
            ('Тег 2', '_' * 201),
            ('Тег 2', 'невалидный_слаг'),
            ('Тег 2', 'invalid slug'),
            ('Тег 2', 'invalid_slug!'),
        ],
    )
    def test_tag_validation_negative(self, name, slug):
        element_count = Tag.objects.count()

        with self.assertRaises(
            ValidationError,
            msg='Validation did not happen',
        ):
            create_and_save_entry(
                Tag,
                name=name,
                slug=slug,
            )

        self.assertEqual(
            Tag.objects.count(),
            element_count,
            msg='There are more elements than there should be',
        )
