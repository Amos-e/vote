# Generated by Django 3.2 on 2022-08-26 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_transactiontype_share_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='all_names',
            field=models.CharField(default='', max_length=255),
        ),
    ]
