# Generated by Django 3.2 on 2021-12-06 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_auto_20211126_2259'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ['-day']},
        ),
    ]
