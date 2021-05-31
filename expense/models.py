from django.contrib.auth import get_user_model
from django.db import models


class Expense(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='expense', on_delete=models.CASCADE)
    day = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    place = models.CharField(max_length=200)
    category = models.PositiveSmallIntegerField()
    priority = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.place} {str(self.amount)}'

