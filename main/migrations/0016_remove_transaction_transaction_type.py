# Generated by Django 3.2 on 2022-08-26 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_transactiontype_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_type',
        ),
    ]
