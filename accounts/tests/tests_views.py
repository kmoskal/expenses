from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models import ActivateAccount
from http.cookies import SimpleCookie
import datetime
import jwt


class TestViews(TestCase):
    def setUp(self):
        self.User = get_user_model()
        user = self.User.objects.create(email='user@user.com')
        user.set_password('foo')
        user.is_active = True
        user.save()
        self.user = user

        self.client = Client()
        response = self.client.post(
            reverse('accounts-get-token'),
            {'email': 'user@user.com', 'password': 'foo'}
        )
        
        self.token = response.json()['access_token']
        self.csrftoken = response.cookies['csrftoken'].value

    def test_register_bad_password(self):
        self.response = self.client.post(
            reverse('accounts-register'),
            {'email': 'new@user.com', 'password': 'foo'}
        )
        self.assertEqual(self.response.status_code, 400)
        self.assertIn('password', self.response.json())

    def test_register_email_already_exists(self):
        self.response = self.client.post(
            reverse('accounts-register'),
            {'email': 'user@user.com', 'password': 'Foobarbaz1'}
        )
        self.assertIn('email', self.response.json())
        self.assertEqual(self.response.status_code, 400)

    def test_update_profile_invalid_data(self):
        data = {
            'first_name': True,
            'last_name': False
        }
        
        self.response = self.client.put(
            reverse('accounts-profile-update'),
            data=data,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(self.response.status_code, 400)

    def test_no_account_to_activate(self):
        self.account = ActivateAccount.objects.first()
        self.response = self.client.get(
            reverse('accounts-activate', kwargs={'token': 'foo'})
        )
        self.assertEqual(self.response.json()['detail'], 'No account to activate')

    def test_refresh_token_view_without_cookies(self):
        # create a new client to delete cookies
        self.c = Client()
        self.response = self.c.post(
            reverse('accounts-refresh-token')
        )
        self.assertEqual(self.response.status_code, 403)
        self.assertIn('detail', self.response.json())
        self.assertNotIn('access_token', self.response.json())

    def test_refresh_token_view_with_expired_token(self):
        payload = {
            'user_id': self.user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=-2),
            'iat': datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        self.client.cookies['refreshtoken'] = refresh_token
        self.response = self.client.post(
            reverse('accounts-refresh-token')
        )
        self.assertEqual(self.response.status_code, 403)
        self.assertIn(self.response.json()['detail'], 'Expired refresh token, please login again.')

    def test_refresh_token_view_user_is_inactive(self):
        # set the id of a user to a non-existent user
        payload = {
            'user_id': 3,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
            'iat': datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        self.client.cookies['refreshtoken'] = refresh_token
        self.response = self.client.post(
            reverse('accounts-refresh-token')
        )
        self.assertEqual(self.response.status_code, 403)
        self.assertIn(self.response.json()['detail'], 'User is inactive')

    def test_get_tokens_view_invalid_email_or_password(self):
        self.response = self.client.post(
            reverse('accounts-get-token'),
            {'email': '', 'password': ''}
        )
        self.assertEqual(self.response.status_code, 403)
        self.assertIn(self.response.json()['detail'], 'Invalid email or password')

    def test_get_tokens_view_no_password(self):
        self.response = self.client.post(
            reverse('accounts-get-token'),
            {'email': 'user@user.com'}
        )
        self.assertEqual(self.response.status_code, 403)
        self.assertIn(self.response.json()['detail'], 'Email/password required')
        
    def test_get_tokens_view_no_email(self):
        self.response = self.client.post(
            reverse('accounts-get-token'),
            {'password': 'foo'}
        )
        self.assertEqual(self.response.status_code, 403)
        self.assertIn(self.response.json()['detail'], 'Email/password required')

    def test_get_tokens_view_bad_password(self):
        self.response = self.client.post(
            reverse('accounts-get-token'),
            {'email': 'user@user.com', 'password': 'baz'}
        )
        self.assertEqual(self.response.status_code, 403)
        self.assertIn(self.response.json()['detail'], 'Invalid email or password')

    def test_get_token_user_is_inactive(self):
        user = self.User.objects.create(email='newuser@user.com')
        user.set_password('foo')
        user.save()
        self.c = Client()
        
        self.response = self.c.post(
            reverse('accounts-get-token'),
            {'email': 'newuser@user.com', 'password': 'foo'}
        )

        self.assertEqual(self.response.status_code, 403)
        self.assertEqual(self.response.json()['detail'], 'User is not active')
