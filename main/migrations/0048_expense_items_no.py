# Generated by Django 3.2 on 2022-12-25 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_auto_20221225_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='items_no',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
