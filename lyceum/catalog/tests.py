from http import HTTPStatus
from random import randint

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
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
        'path, pk, expected_content, status',
        [
            ('', '', 'Список элементов', HTTPStatus.OK),
            ('', *([randint(1, 100)] * 2), HTTPStatus.OK),
            ('re/', *([randint(1, 100)] * 2), HTTPStatus.OK),
            ('re/', -1, None, HTTPStatus.NOT_FOUND),
            ('re/', '', None, HTTPStatus.NOT_FOUND),
            ('re/', 'qwerty', None, HTTPStatus.NOT_FOUND),
            ('converter/', *([randint(1, 100)] * 2), HTTPStatus.OK),
            ('converter/', -1, None, HTTPStatus.NOT_FOUND),
            ('converter/', '', None, HTTPStatus.NOT_FOUND),
            ('converter/', 'qwerty', None, HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_response(self, path, pk, expected_content, status):
        end = '' if pk == '' else '/'
        response = self.client.get('/catalog/' + path + str(pk) + end)
        self.assertEqual(response.status_code, status)
        if status == HTTPStatus.OK:
            self.assertIn(
                str(expected_content).encode('utf-8'),
                response.content,
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
        'first_name, second_name, slug, weight',
        [
            ('Категория 1', 'Категория_1', 'category-1', 100),
            ('Категория 1', 'Категория 1!', 'category-2', 100),
            ('Категория 1', 'категория 1', 'category-3', 100),
            ('Категория 1', 'Kатегория 1', 'category-4', 100),
        ],
    )
    def test_category_normalized_name(
        self,
        first_name,
        second_name,
        slug,
        weight,
    ):

        create_and_save_entry(
            Category,
            name=first_name,
            slug=slug,
            weight=weight,
        )

        element_count = Category.objects.count()

        with self.assertRaises(ValidationError):
            create_and_save_entry(
                Category,
                name=second_name,
                slug=slug,
                weight=weight,
            )

        self.assertEqual(Category.objects.count(), element_count)

    @parametrize(
        'first_name, second_name, slug',
        [
            ('Тег 1', 'Тег_1', 'tag-1'),
            ('Тег 1', 'Тег 1!', 'tag-2'),
            ('Тег 1', 'тег 1', 'tag-3'),
            ('Тег 1', 'Tег 1', 'tag-4'),
        ],
    )
    def test_tag_normalized_name(
        self,
        first_name,
        second_name,
        slug,
    ):

        create_and_save_entry(Tag, name=first_name, slug=slug)

        element_count = Tag.objects.count()

        with self.assertRaises(ValidationError):
            create_and_save_entry(Tag, name=second_name, slug=slug)

        self.assertEqual(Tag.objects.count(), element_count)
