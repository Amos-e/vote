# Generated by Django 3.2 on 2023-01-13 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0067_auto_20230113_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]