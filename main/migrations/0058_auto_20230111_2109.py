# Generated by Django 3.2 on 2023-01-11 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_rename_ineterest_loan_interest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='other_reason',
            new_name='notes',
        ),
    ]
