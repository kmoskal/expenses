# Generated by Django 3.2 on 2021-11-11 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='priority',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
