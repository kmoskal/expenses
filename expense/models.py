from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name='category', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Priority(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name='priority', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name='expense', on_delete=models.CASCADE
    )
    day = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    place = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, blank=True,
        null=True, on_delete=models.CASCADE
    )
    priority = models.ForeignKey(
        Priority, blank=True,
        null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.place} {str(self.price)}'
