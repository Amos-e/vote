# Generated by Django 3.2 on 2023-03-04 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0090_auto_20230303_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
