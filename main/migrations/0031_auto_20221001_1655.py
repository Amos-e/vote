# Generated by Django 3.2 on 2022-10-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_rename_others_member_other'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='other',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='other_reason',
            field=models.TextField(blank=True, default='Other Reason'),
        ),
    ]
