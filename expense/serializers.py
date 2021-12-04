from rest_framework import serializers
from .models import Expense, Category, Priority


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'day', 'price', 'place', 'category', 'priority')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('id', 'name')
