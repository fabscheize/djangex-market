from django.test import Client, override_settings, TestCase


class ReverseMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_middleware_on(self):
        for _ in range(9):
            response = self.client.get('/coffee/')
            self.assertIn('Я чайник'.encode('utf-8'), response.content)

        response = self.client.get('/coffee/')
        self.assertIn('Я кинйач'.encode('utf-8'), response.content)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_middleware_oаа(self):
        for _ in range(10):
            response = self.client.get('/coffee/')
            self.assertIn('Я чайник'.encode('utf-8'), response.content)
