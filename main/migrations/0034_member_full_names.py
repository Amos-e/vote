# Generated by Django 3.2 on 2022-12-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_remove_member_all_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='full_names',
            field=models.CharField(default='', max_length=255),
        ),
    ]
