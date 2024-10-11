from django.test import Client, override_settings, TestCase
from parametrize import parametrize


class ReverseMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()

    @parametrize(
        'allow_reverse, expected_content',
        [
            (True, 'Я кинйач'),
            (False, 'Я чайник'),
        ],
    )
    def test_reverse_middleware(self, allow_reverse, expected_content):
        phrase = 'Я чайник'
        with override_settings(ALLOW_REVERSE=allow_reverse):
            for i in range(1, 11):
                if i == 10:
                    phrase = expected_content
                response = self.client.get('/coffee/')
                self.assertIn(phrase.encode('utf-8'), response.content)
