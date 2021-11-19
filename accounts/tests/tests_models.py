from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import CustomUser, ActivateAccount


class ModelsTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(email='user@user.com', password='foo')
        ActivateAccount.objects.create(email='user@user.com')

    def test_customuser_str_returns(self):
        self.user = CustomUser.objects.first()
        self.assertEqual(str(self.user), 'user@user.com')


    def test_activate_account_str_returns(self):
        self.aa = ActivateAccount.objects.first()
        self.assertEqual(str(self.aa), f'user@user.com created at {self.aa.create_date}')
