from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import ActivateAccount


class TestUrls(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(email='user@user.com')
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

    def test_get_token(self):
        self.response = self.client.post(
            reverse('accounts-get-token'),
            {'email': 'user@user.com', 'password': 'foo'}
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('access_token', self.response.json())
        self.assertIn('refreshtoken', self.response.cookies)
        self.assertIn('csrftoken', self.response.cookies)

    def test_refresh_token(self):
        self.response = self.client.post(
            reverse('accounts-refresh-token'),
            **{'X-CSRFToken': self.csrftoken}
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('access_token', self.response.json())

    def test_profile(self):
        self.response = self.client.get(
            reverse('accounts-profile'),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.json()['user']['email'],
                         'user@user.com')

    def test_update_profile(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe'
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
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.json()['first_name'], 'John')
        self.assertEqual(self.response.json()['last_name'], 'Doe')

    def test_register_status_201(self):
        self.response = self.client.post(
            reverse('accounts-register'),
            {'email': 'new@user.com', 'password': 'Foobarbaz1'}
        )
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.json()['id'], 2)

    def test_activate_account(self):
        self.client.post(reverse('accounts-register'),
                         {'email': 'user1@user.com', 'password': 'Foobarbaz1'})
        self.aa_token = ActivateAccount.objects.first().token
        self.response = self.client.get(
            reverse('accounts-activate', kwargs={'token': self.aa_token})
        )
        self.assertEqual(self.response.status_code, 200)
