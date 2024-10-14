from django.http import HttpResponse
from django.test import Client, override_settings, RequestFactory, TestCase
from lyceum.middleware import ReverseMiddleware
from parametrize import parametrize


class ReverseMiddlewareTest(TestCase):

    @parametrize(
        'allow_reverse, expected_normal, expected_reversed',
        [
            (True, 9, 1),
            (False, 10, 0),
        ],
    )
    def test_reverse_middleware(
        self, allow_reverse, expected_normal, expected_reversed
    ):
        responses = {'Я чайник': 0, 'Я кинйач': 0}

        with override_settings(ALLOW_REVERSE=allow_reverse):
            for _ in range(10):
                response = Client().get('/coffee/')
                key = response.content.decode('utf-8').strip('</body>')
                responses[key] += 1

        self.assertEqual(expected_normal, responses['Я чайник'])
        self.assertEqual(expected_reversed, responses['Я кинйач'])

    @parametrize(
        'initial_content, expected_content',
        [
            ('дддFFFддд', 'дддFFFддд'),
            ('Данила, привет!', 'алинаД, тевирп!'),
            ('Тест-реверса', 'тсеТ-асревер'),
            (
                '0чень "интересный",пример арбуz',
                '0чень "йынсеретни",ремирп арбуz',
            ),
        ],
    )
    def test_middleware_reverses_content_on_tenth_request(
        self, initial_content, expected_content
    ):
        factory = RequestFactory()
        middleware = ReverseMiddleware(
            lambda request: HttpResponse(initial_content)
        )
        ReverseMiddleware.count = 9
        request = factory.get('/')
        response = middleware(request)
        self.assertIn(expected_content, response.content.decode('utf-8'))
