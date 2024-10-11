from django.test import Client, override_settings, TestCase
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
