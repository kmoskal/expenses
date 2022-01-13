from django.urls import path
from .views import (
    ExpensesList, ExpenseDetail,
    CategoryList, CategoryDetail,
    PriorityList, PriorityDetail,
    SummaryMonthlyExpenses,
)

urlpatterns = [
    path('', ExpensesList.as_view(), name='expense-expense-list'),
    path('expense/<int:pk>', ExpenseDetail.as_view(),
         name='expense-expense-detail'),
    path('category', CategoryList.as_view(), name='expense-category-list'),
    path('category/<int:pk>', CategoryDetail.as_view(),
         name='expense-category-detail'),
    path('priority', PriorityList.as_view(), name='expense-priority-list'),
    path('priority/<int:pk>', PriorityDetail.as_view(),
         name='expense-priority-detail'),
    path('summary', SummaryMonthlyExpenses.as_view(), name='expense-monthly-summary'),
]

