# Generated by Django 3.2 on 2022-09-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20220922_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='tulinaawecontributor',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
