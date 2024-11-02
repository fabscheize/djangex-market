from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from parametrize import parametrize

from lyceum.middleware import ReverseMiddleware

__all__ = []


class ReverseMiddlewareTest(TestCase):
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
        self,
        initial_content,
        expected_content,
    ):
        factory = RequestFactory()
        middleware = ReverseMiddleware(
            lambda request: HttpResponse(initial_content),
        )
        ReverseMiddleware.count = 9
        request = factory.get(reverse('homepage:home'))
        response = middleware(request)
        self.assertIn(expected_content, response.content.decode('utf-8'))
