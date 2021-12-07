from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlencode
from datetime import date

from expense.models import Expense, Category, Priority


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        user = cls.User.objects.create(email='user@user.com')
        user.set_password('foo')
        user.is_active = True
        user.save()
        cls.user = user

        cls.category = Category.objects.create(user=cls.user, name='Food')
        cls.priority = Priority.objects.create(user=cls.user, name='High')

        for i in range(6):
            Expense.objects.create(
                user=cls.user, price=10 + i, place='Shop' + str(i),
                category=cls.category,
                priority=cls.priority
            )

        # change year to check query params when getting expenses
        cls.expense = Expense.objects.get(pk=6)
        cls.expense.day = date(cls.expense.day.year-1,
                               cls.expense.day.month,
                               cls.expense.day.day)
        cls.expense.save()

    def setUp(self):
        self.client = Client()
        response = self.client.post(
            reverse('accounts-get-token'),
            {'email': 'user@user.com', 'password': 'foo'}
        )

        self.token = response.json()['access_token']
        self.csrftoken = response.cookies['csrftoken'].value

    def test_post_category_list(self):
        data = {'name': 'Drink'}

        response = self.client.post(
            reverse('expense-category-list'),
            data=data,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_post_category_list_without_required_fields(self):
        data = {}

        response = self.client.post(
            reverse('expense-category-list'),
            data=data,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_post_category_list_name_field_isnt_string(self):
        data = {'name': False}

        response = self.client.post(
            reverse('expense-category-list'),
            data=data,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_get_category_list(self):
        response = self.client.get(
            reverse('expense-category-list'),
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_category_detail(self):
        response = self.client.get(
            reverse('expense-category-detail', kwargs={'pk': 1}),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_get_category_detail_no_data(self):
        response = self.client.get(
            reverse('expense-category-detail', kwargs={'pk': 10}),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())

    def test_update_category_detail(self):
        data = {'name': 'food'}

        response = self.client.put(
            reverse('expense-category-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data=data,
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CRSFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'food')

    def test_update_category_detail_no_data(self):
        data = {}

        response = self.client.put(
            reverse('expense-category-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data=data,
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CRSFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_update_category_detail_invalid_data(self):
        data = {'name': False}

        response = self.client.put(
            reverse('expense-category-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data=data,
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CRSFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_delete_category(self):
        response = self.client.delete(
            reverse('expense-category-detail', kwargs={'pk': 1}),
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_category_non_existing_id(self):
        response = self.client.delete(
            reverse('expense-category-detail', kwargs={'pk': 10}),
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())

    def test_post_priority_list(self):
        data = {'name': 'High'}

        response = self.client.post(
            reverse('expense-priority-list'),
            data=data,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_post_priority_list_without_required_fields(self):
        data = {}

        response = self.client.post(
            reverse('expense-priority-list'),
            data=data,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_post_priority_list_name_field_isnt_string(self):
        data = {'name': False}

        response = self.client.post(
            reverse('expense-priority-list'),
            data=data,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_get_priority_list(self):
        response = self.client.get(
            reverse('expense-priority-list'),
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_priority_detail(self):
        response = self.client.get(
            reverse('expense-priority-detail', kwargs={'pk': 1}),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_get_priority_detail_no_data(self):
        response = self.client.get(
            reverse('expense-priority-detail', kwargs={'pk': 10}),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())

    def test_update_priority_detail(self):
        data = {'name': 'high'}

        response = self.client.put(
            reverse('expense-priority-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data=data,
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CRSFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'high')

    def test_update_priority_detail_no_data(self):
        data = {}

        response = self.client.put(
            reverse('expense-priority-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data=data,
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CRSFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_update_priority_detail_invalid_data(self):
        data = {'name': False}

        response = self.client.put(
            reverse('expense-priority-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data=data,
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CRSFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.json())

    def test_delete_priority(self):
        response = self.client.delete(
            reverse('expense-priority-detail', kwargs={'pk': 1}),
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_priority_non_existing_id(self):
        response = self.client.delete(
            reverse('expense-priority-detail', kwargs={'pk': 10}),
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())

    def test_get_all_expenses(self):
        response = self.client.get(
            reverse('expense-expense-list'),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 5)

    def test_get_expenses_with_query_param_year_passed(self):
        params = urlencode({'year': date.today().year - 1})
        response = self.client.get(
            reverse('expense-expense-list') + '?' + params,
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

    def test_get_expenses_with_query_param_year_out_of_range(self):
        params = urlencode({'year': 0})
        response = self.client.get(
            reverse('expense-expense-list') + '?' + params,
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 404)

    def test_get_expenses_with_query_param_month_passed(self):
        params = urlencode({'month': date.today().month})
        response = self.client.get(
            reverse('expense-expense-list') + '?' + params,
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 5)

    def test_get_expenses_with_query_param_month_out_of_range(self):
        params = urlencode({'month': 0})
        response = self.client.get(
            reverse('expense-expense-list') + '?' + params,
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 404)

    def test_get_all_expenses_with_pagination_limit(self):
        limit = 1
        params = urlencode({'limit': limit})
        response = self.client.get(
            reverse('expense-expense-list') + '?' + params,
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), limit)

    def test_get_expenses_when_no_expenses(self):
        expenses = Expense.objects.all()
        expenses.delete()

        response = self.client.get(
            reverse('expense-expense-list'),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 200)

    def test_add_expense(self):
        expense = {
            'place': 'Shop6',
            'price': 15
        }

        response = self.client.post(
            reverse('expense-expense-list'),
            content_type='application/json',
            data=expense,
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.json()['id'], 7)
        self.assertEqual(response.status_code, 201)

    def test_add_expense_without_data(self):
        expense = {}
        response = self.client.post(
            reverse('expense-expense-list'),
            content_type='application/json',
            data=expense,
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertCountEqual(['price', 'place'], response.json())

    def test_get_expense_detail(self):
        response = self.client.get(
            reverse('expense-expense-detail', kwargs={'pk': 2}),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 2)

    def test_get_expense_detail_when_no_expense(self):
        response = self.client.get(
            reverse('expense-expense-detail', kwargs={'pk': 10}),
            **{'HTTP_AUTHORIZATION': 'Bearer ' + self.token}
        )

        self.assertIn('detail', response.json())
        self.assertEqual(response.status_code, 404)

    def test_update_expense(self):
        expense = {
            'price': 30,
            'place': 'ShopUpdated'
        }
        response = self.client.put(
            reverse('expense-expense-detail', kwargs={'pk': 2}),
            data=expense,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['place'], 'ShopUpdated')

    def test_update_expense_with_no_data(self):
        expense = {}

        response = self.client.put(
            reverse('expense-expense-detail', kwargs={'pk': 2}),
            data=expense,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertCountEqual(['price', 'place'], response.json())

    def test_update_expense_with_bad_data(self):
        expense = {
            'price': '30',
            'place': 'ShopUpdated',
            'category': 'Food'
        }

        response = self.client.put(
            reverse('expense-expense-detail', kwargs={'pk': 2}),
            data=expense,
            content_type='application/json',
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('category', response.json())

    def test_delete_expense(self):
        response = self.client.delete(
            reverse('expense-expense-detail', kwargs={'pk': 2}),
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_expense_wrong_id(self):
        response = self.client.delete(
            reverse('expense-expense-detail', kwargs={'pk': 10}),
            **{
                'HTTP_AUTHORIZATION': 'Bearer ' + self.token,
                'X-CSRFToken': self.csrftoken
            }
        )

        self.assertEqual(response.status_code, 404)
