from django.test import TestCase, Client


class AboutHttpResponseTest(TestCase):
    def test_about_status_code(self):
        response = Client().get('/about/')
        self.assertEqual(response.status_code, 200)
