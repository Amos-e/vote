# Generated by Django 3.2 on 2022-09-25 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_alter_transaction_other_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='others',
            field=models.IntegerField(default=0),
        ),
    ]
