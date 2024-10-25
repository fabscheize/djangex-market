from http import HTTPStatus
from random import randint

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import NoReverseMatch, reverse
from parametrize import parametrize

from catalog.models import Category, Item, Tag


def create_and_save_entry(model_class, **kwargs):
    instance = model_class(**kwargs)
    instance.full_clean()
    instance.save()


class CatalogHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    @parametrize(
        'path, pk, expected_content',
        [
            ('item', *([randint(1, 5)] * 2)),
            ('re_item', *([randint(1, 5)] * 2)),
            ('c_item', *([randint(1, 5)] * 2)),
        ],
    )
    def test_catalog_response_positive(self, path, pk, expected_content):
        response = self.client.get(reverse('catalog:' + path, args=[str(pk)]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            str(expected_content).encode('utf-8'),
            response.content,
        )

    @parametrize(
        'path, pk',
        [
            ('re_item', -1),
            ('re_item', ''),
            ('re_item', 'qwerty'),
            ('c_item', -1),
            ('c_item', ''),
            ('c_item', 'qwerty'),
        ],
    )
    def test_catalog_response_negative(self, path, pk):
        with self.assertRaises(NoReverseMatch):
            self.client.get(
                reverse('catalog:' + path, args=[str(pk)]),
            )


class CategoryModelTest(TestCase):
    @parametrize(
        'name, slug, weight, created_elements',
        [
            ('Категория 1', 'category-1', 100, 1),
            ('А' * 150, 'category-1', 100, 1),
            ('А' * 151, 'category-2', 100, 0),
            ('Категория 2', '_' * 200, 100, 1),
            ('Категория 2', '_' * 201, 100, 0),
            ('Категория 2', 'невалидный_слаг', 100, 0),
            ('Категория 2', 'invalid slug', 100, 0),
            ('Категория 2', 'invalid_slug!', 100, 0),
            ('Категория 3', 'category-3', 0, 0),
            ('Категория 3', 'category-3', 1, 1),
        ],
    )
    def test_category_validation(self, name, slug, weight, created_elements):
        element_count = Category.objects.count()

        if created_elements == 0:
            with self.assertRaises(ValidationError):
                create_and_save_entry(
                    Category,
                    name=name,
                    slug=slug,
                    weight=weight,
                )
        else:
            create_and_save_entry(
                Category,
                name=name,
                slug=slug,
                weight=weight,
            )

        self.assertEqual(
            Category.objects.count(),
            element_count + created_elements,
        )


class TagModelTest(TestCase):
    @parametrize(
        'name, slug, created_elements',
        [
            ('Тег 1', 'tag-1', 1),
            ('А' * 150, 'tag-2', 1),
            ('А' * 151, 'tag-2', 0),
            ('Тег 2', '_' * 200, 1),
            ('Тег 2', '_' * 201, 0),
            ('Тег 2', 'невалидный_слаг', 0),
            ('Тег 2', 'invalid slug', 0),
            ('Тег 2', 'invalid_slug!', 0),
        ],
    )
    def test_tag_validation(self, name, slug, created_elements):
        element_count = Tag.objects.count()

        if created_elements == 0:
            with self.assertRaises(ValidationError):
                create_and_save_entry(
                    Tag,
                    name=name,
                    slug=slug,
                )
        else:
            create_and_save_entry(
                Tag,
                name=name,
                slug=slug,
            )

        self.assertEqual(Tag.objects.count(), element_count + created_elements)


class ItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Категория',
            slug='category',
            weight=100,
        )

    @parametrize(
        'name, text, created_elements',
        [
            ('Товар 1', 'Это превосходно оформленный товар.', 1),
            ('Товар 2', 'Роскошно иметь такой товар.', 1),
            ('A' * 150, 'Это превосходно оформленный товар.', 1),
            ('A' * 151, 'Это превосходно оформленный товар.', 0),
            ('Товар 3', 'Отстойный товар без нужных слов.', 0),
            ('Товар 3', 'Ппревосходно превосх0дно роскошно0', 0),
        ],
    )
    def test_item_validation(self, name, text, created_elements):
        element_count = Item.objects.count()

        if created_elements == 0:
            with self.assertRaises(ValidationError):
                create_and_save_entry(
                    Item,
                    name=name,
                    text=text,
                    category=self.category,
                )
        else:
            create_and_save_entry(
                Item,
                name=name,
                text=text,
                category=self.category,
            )

        self.assertEqual(
            Item.objects.count(),
            element_count + created_elements,
        )


class NormalizedNameTest(TestCase):
    @parametrize(
        'first_name, second_name',
        [
            ('Категория 1', 'Категория_1'),
            ('Категория 1', 'Категория 1!'),
            ('Категория 1', 'категория 1'),
            ('Категория 1', 'Kатегория 1'),
        ],
    )
    def test_category_normalized_name(
        self,
        first_name,
        second_name,
    ):

        create_and_save_entry(
            Category,
            name=first_name,
            slug='category-1',
            weight=100,
        )

        element_count = Category.objects.count()

        with self.assertRaises(ValidationError):
            create_and_save_entry(
                Category,
                name=second_name,
                slug='category-2',
                weight=100,
            )

        self.assertEqual(Category.objects.count(), element_count)

    @parametrize(
        'first_name, second_name',
        [
            ('Тег 1', 'Тег_1'),
            ('Тег 1', 'Тег 1!'),
            ('Тег 1', 'тег 1'),
            ('Тег 1', 'Tег 1'),
        ],
    )
    def test_tag_normalized_name(
        self,
        first_name,
        second_name,
    ):

        create_and_save_entry(Tag, name=first_name, slug='tag-1')

        element_count = Tag.objects.count()

        with self.assertRaises(ValidationError):
            create_and_save_entry(Tag, name=second_name, slug='tag-2')

        self.assertEqual(Tag.objects.count(), element_count)
        self.assertEqual(Tag.objects.count(), element_count)
