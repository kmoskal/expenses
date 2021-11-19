from django.test import TestCase
from django.contrib.auth import get_user_model
from expense.models import Category, Priority, Expense


class ModelsTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create(
            email='user@user.com', password='foo'
        )
        Expense.objects.create(user=self.user, price=10, place='Amazon')
        Category.objects.create(user=self.user, name='Food')
        Priority.objects.create(user=self.user, name='High')

    def test_expense_str_method_returns(self):
        self.assertEqual(str(Expense.objects.first()), 'Amazon 10.00')

    def test_category_str_method_returns(self):
        self.assertEqual(str(Category.objects.first()), 'Food')

    def test_priority_str_method_returns(self):
        self.assertEqual(str(Priority.objects.first()), 'High')
