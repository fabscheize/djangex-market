from http import HTTPStatus
from random import randint

from django.test import Client, TestCase
from parametrize import parametrize


class CatalogHttpResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    @parametrize(
        'path, pk, expected_content, status',
        [
            ('', '', 'Список элементов', HTTPStatus.OK),
            ('', randint(0, 100), 'Подробно элемент', HTTPStatus.OK),
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
                str(expected_content).encode('utf-8'), response.content
            )
