# Generated by Django 3.2 on 2022-12-25 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_expense_expenseitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='_from',
            field=models.CharField(default='None', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expense',
            name='_to',
            field=models.CharField(default='None', max_length=255),
            preserve_default=False,
        ),
    ]