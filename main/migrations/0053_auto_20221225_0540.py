# Generated by Django 3.2 on 2022-12-25 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_auto_20221225_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='_from',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AlterField(
            model_name='expense',
            name='_to',
            field=models.CharField(default=' ', max_length=255),
        ),
    ]