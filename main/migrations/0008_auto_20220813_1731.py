# Generated by Django 3.2 on 2022-08-13 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210605_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberdetail',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='members',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
