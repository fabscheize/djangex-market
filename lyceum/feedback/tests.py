from django.test import TestCase
from django.urls import reverse
from parametrize import parametrize

from feedback import forms

__all__ = []


class FeedbackFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.feedback_form = forms.FeedbackForm()

    def test_correct_context(self):
        response = self.client.get(reverse('feedback:feedback'))
        self.assertIn('form', response.context, msg='No form in context')

    @parametrize(
        'field, label',
        [
            ('name', 'Ваше имя'),
            ('mail', 'Ваша электронная почта'),
            ('text', 'Ваш вопрос или пожелание'),
        ],
    )
    def test_form_labels(self, field, label):
        received = type(self).feedback_form.fields[field].label
        self.assertEqual(
            received,
            label,
            msg=f'Expected "{label}" {field} label, got "{received}"',
        )

    @parametrize(
        'field, help_text',
        [
            ('mail', 'name@example.com'),
        ],
    )
    def test_form_help_texts(self, field, help_text):
        received = type(self).feedback_form.fields[field].help_text
        self.assertEqual(
            received,
            help_text,
            msg=f'Expected "{help_text}" {field} help_text, got "{received}"',
        )

    def test_create_feedback_negative(self):
        form_data = {
            'name': 'name',
            'mail': 'invalid_mail',
            'text': 'text',
        }

        response = self.client.post(
            reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )

        self.assertTrue(
            response.context['form'].has_error('mail'),
            msg='Mail validation did not happen',
        )

    def test_create_feedback_positive(self):
        form_data = {
            'name': 'name',
            'mail': 'name@mail.com',
            'text': 'text',
        }

        response = self.client.post(
            reverse('feedback:feedback'),
            data=form_data,
        )

        self.assertRedirects(
            response,
            reverse('feedback:feedback'),
        )
