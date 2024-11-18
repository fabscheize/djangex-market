from pathlib import Path
from tempfile import TemporaryDirectory

from django.conf import settings
from django.core.files.base import ContentFile
from django.test import override_settings, TestCase
from django.urls import reverse
from parametrize import parametrize

from feedback import forms, models


__all__ = []


class FeedbackFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.feedback_form = forms.FeedbackForm()
        cls.feedback_author_form = forms.FeedbackAuthorForm()
        cls.feedback_file_form = forms.FeedbackFileForm()

    def test_correct_context(self):
        response = self.client.get(reverse('feedback:feedback'))
        self.assertIn('form', response.context, msg='No form in context')

    @parametrize(
        'form, field, label',
        [
            ('feedback_author_form', 'name', 'Ваше имя'),
            ('feedback_author_form', 'mail', 'Ваша электронная почта'),
            ('feedback_form', 'text', 'Ваш вопрос или пожелание'),
            (
                'feedback_file_form',
                'files',
                'При необходимости прикрепите файлы',
            ),
        ],
    )
    def test_form_labels(self, form, field, label):
        received = eval(f'self.{form}.fields[field].label')

        self.assertEqual(
            received,
            label,
            msg=f'Expected "{label}" {field} label, got "{received}"',
        )

    @parametrize(
        'form, field, help_text',
        [
            ('feedback_author_form', 'mail', 'Обязательное поле'),
            ('feedback_form', 'text', 'Обязательное поле'),
        ],
    )
    def test_form_help_texts(self, form, field, help_text):
        received = eval(f'self.{form}.fields[field].help_text')

        self.assertEqual(
            received,
            help_text,
            msg=f'Expected "{help_text}" {field} help_text, got "{received}"',
        )

    def test_create_feedback_negative(self):
        element_count = models.Feedback.objects.count()

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
            response.context['feedback_author_form'].has_error('mail'),
            msg='Mail validation did not happen',
        )

        self.assertEqual(
            models.Feedback.objects.count(),
            element_count,
            msg='There are more elements than there should be',
        )

    def test_create_feedback_positive(self):
        element_count = models.Feedback.objects.count()

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

        self.assertEqual(
            models.Feedback.objects.count(),
            element_count + 1,
            msg='New object has not been created',
        )

    @override_settings(MEDIA_ROOT=TemporaryDirectory().name)
    def test_file_upload(self):
        num_of_files = 5

        files = [
            ContentFile(f'file_{i}'.encode(), name='filename')
            for i in range(num_of_files)
        ]

        form_data = {
            'name': 'name',
            'mail': 'name@mail.com',
            'text': 'text',
            'files': files,
        }

        self.client.post(
            reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )

        file_object = models.Feedback.objects.get(text='text')

        self.assertEqual(
            file_object.files.count(),
            num_of_files,
            msg='There are more elements than there should be',
        )

        media_root = Path(settings.MEDIA_ROOT)

        for i, file in enumerate(file_object.files.all()):
            uploaded_file = media_root / file.file.path
            self.assertEqual(
                uploaded_file.open().read(),
                f'file_{i}',
            )
