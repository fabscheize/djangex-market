import datetime
from unittest import mock

import django.test
from django.urls import reverse
from parametrize import parametrize
import pytz

from users.models import User


__all__ = []


class UserRegistrationTest(django.test.TestCase):
    @parametrize(
        'username, email, password1, password2',
        [
            (
                'test_user',
                'testuser@example.com',
                'StrongPass123!',
                'StrongPass123!',
            ),
        ],
    )
    def test_user_registration_positive(
        self,
        username,
        email,
        password1,
        password2,
    ):
        with django.test.override_settings(DEFAULT_USER_ACTIVITY='False'):
            self.client.post(
                reverse('users:signup'),
                {
                    'username': username,
                    'email': email,
                    'password1': password1,
                    'password2': password2,
                },
                follow=True,
            )

            user = User.objects.get(username=username)
            self.assertIsNotNone(user, msg='User was not created')
            self.assertEqual(
                user.email,
                email,
                msg="User's email is incorrect",
            )
            self.assertFalse(
                user.is_active,
                msg='User is unexpectly activated',
            )

    @parametrize(
        'username, email, password1, password2',
        [
            (
                'test_user',
                'testuser@example.com',
                'StrongPass123!',
                'DifferentPass123!',
            ),
            (
                'test_user',
                'not-an-email',
                'StrongPass123!',
                'StrongPass123!',
            ),
            (
                'test_user',
                'testuser@example.com',
                'short',
                'short',
            ),
        ],
    )
    def test_user_registration_negative(
        self,
        username,
        email,
        password1,
        password2,
    ):
        with django.test.override_settings(DEFAULT_USER_ACTIVITY='False'):
            self.client.post(
                reverse('users:signup'),
                {
                    'username': username,
                    'email': email,
                    'password1': password1,
                    'password2': password2,
                },
                follow=True,
            )

            with self.assertRaises(
                User.DoesNotExist,
                msg='User was unexpectly created',
            ):
                User.objects.get(username=username)


class UserActivationTest(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        django.test.Client().post(
            reverse('users:signup'),
            {
                'username': 'user',
                'email': 'user@example.com',
                'password1': 'AA385W3ersHHGv',
                'password2': 'AA385W3ersHHGv',
            },
            follow=True,
        )

    @django.test.override_settings(DEFAULT_USER_ACTIVITY='False')
    @mock.patch('django.utils.timezone.now')
    def test_user_activation_positive(self, mock_now):
        user = User.objects.get(username='user')
        self.assertFalse(user.is_active, msg='User already active')

        mock_now.return_value = pytz.UTC.localize(
            django.utils.timezone.datetime.now() + datetime.timedelta(),
        )

        django.test.Client().get(
            reverse('users:activate', args=(user.username,)),
            follow=True,
        )

        user.refresh_from_db()
        self.assertTrue(user.is_active, msg='User was not activated')

    @django.test.override_settings(DEFAULT_USER_ACTIVITY='False')
    @mock.patch('django.utils.timezone.now')
    def test_user_activation_negative(self, mock_now):
        user = User.objects.get(username='user')
        self.assertFalse(user.is_active, msg='User already active')

        mock_now.return_value = pytz.UTC.localize(
            django.utils.timezone.datetime.now()
            + datetime.timedelta(hours=12),
        )

        django.test.Client().get(
            reverse('users:activate', args=(user.username,)),
            follow=True,
        )

        user.refresh_from_db()
        self.assertFalse(user.is_active, msg='User was unexpectly activated')
