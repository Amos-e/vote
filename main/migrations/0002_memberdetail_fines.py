# Generated by Django 2.2 on 2021-05-31 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberdetail',
            name='fines',
            field=models.IntegerField(default=0),
        ),
    ]