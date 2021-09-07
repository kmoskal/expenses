from django.urls import path
from .views import (
    ExpensesList, ExpenseDetail,
    CategoryList, CategoryDetail,
    PriorityList, PriorityDetail,
)

urlpatterns = [
    path('', ExpensesList.as_view()),
    path('expense/<int:pk>', ExpenseDetail.as_view()),
    path('category', CategoryList.as_view()),
    path('category/<int:pk>', CategoryDetail.as_view()),
    path('priority', PriorityList.as_view()),
    path('priority/<int:pk>', PriorityDetail.as_view()),
]
