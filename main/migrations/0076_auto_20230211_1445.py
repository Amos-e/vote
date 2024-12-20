# Generated by Django 3.2 on 2023-02-11 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0075_alter_loan_date_when_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='member_interest_rate',
            field=models.IntegerField(default=0.2),
        ),
        migrations.AddField(
            model_name='loan',
            name='non_member_interest_rate',
            field=models.IntegerField(default=0.3),
        ),
    ]
