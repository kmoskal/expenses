from django.http import Http404
from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Expense, Priority
from .serializers import (
        CategorySerializer, ExpenseSerializer, PrioritySerializer
)
from .utils import create_date_range


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class CategoryList(APIView):
    # List all category or create a new one
    def get(self, request, format=None):
        category = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    """
    Retrieve, update, or delete a category instance
    """
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PriorityList(APIView):
    # List all priority or create a new one
    def get(self, request, format=None):
        priority = Priority.objects.filter(user=request.user)
        serializer = PrioritySerializer(priority, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PrioritySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriorityDetail(APIView):
    """
    Retrieve, update, or delete a priority instance
    """
    def get_object(self, pk):
        try:
            return Priority.objects.get(pk=pk)
        except Priority.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        priority = self.get_object(pk)
        serializer = PrioritySerializer(priority)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        priority = self.get_object(pk)
        serializer = PrioritySerializer(priority, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        priority = self.get_object(pk)
        priority.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpensesList(APIView):
    """
    List all expenses or create a new one
    """
    pagination_class = BasicPagination
    serializer_class = ExpenseSerializer

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request,
                                                view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request, format=None):
        date_range = create_date_range(self.request.query_params)
        expenses = Expense.objects.filter(day__range=date_range)

        if self.request.GET.get('cat'):
            expenses = expenses.filter(category_id=self.request.GET.get('cat'))

        if self.request.GET.get('pri'):
            expenses = expenses.filter(priority_id=self.request.GET.get('pri'))

        page = self.paginate_queryset(expenses)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(
                page, many=True).data
            )
        else:
            serializer = self.serializer_class(expenses, many=True)

        # performing calculations for statistic
        expenses_sum = expenses.aggregate(Sum('price'))

        mostly_chosen_category = expenses.values('category'). \
                annotate(Count('category')).order_by('-category__count')
        if mostly_chosen_category:
            mostly_chosen_category = mostly_chosen_category[0]

        mostly_chosen_priority = expenses.values('priority'). \
                annotate(Count('priority')).order_by('-priority__count')
        if mostly_chosen_priority:
            mostly_chosen_priority = mostly_chosen_priority[0]

        mostly_chosen_place = expenses.values('place'). \
                annotate(Count('place')).order_by('-place__count')
        if mostly_chosen_place:
            mostly_chosen_place = mostly_chosen_place[0]

        updated_serializer = {'date_range': date_range}
        updated_serializer.update({'statistics': {}})
        updated_serializer['statistics'].update(expenses_sum)
        updated_serializer['statistics'].update(mostly_chosen_place)
        updated_serializer['statistics'].update(mostly_chosen_category)
        updated_serializer['statistics'].update(mostly_chosen_priority)
        updated_serializer.update(serializer.data)

        return Response(updated_serializer)

    def post(self, request, format=None):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetail(APIView):
    """
    Retrieve, update, or delete a expense instance
    """
    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        expense = self.get_object(pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
