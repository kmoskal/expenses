from django.urls import path
from .views import ExpensesList, ExpenseDetail

urlpatterns = [
    path('', ExpensesList.as_view()),
    path('expense/<int:pk>', ExpenseDetail.as_view()),
]
