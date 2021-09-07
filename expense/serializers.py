from rest_framework import serializers
from .models import Expense, Category, Priority


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'day', 'price', 'place', 'category', 'priority')

    def create(self, validated_data):
        return Expense.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('id', 'name')

    def create(self, validated_data):
        return Priority.objects.create(**validated_data)
