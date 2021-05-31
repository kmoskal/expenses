from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'day', 'price', 'place', 'category', 'priority')

    def create(self, validated_data):
        return Expense.objects.create(**validated_data)

