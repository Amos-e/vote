# Generated by Django 2.2 on 2021-06-01 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_memberdetail_fine_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberdetail',
            name='fine_type',
            field=models.CharField(choices=[('General_Meeting', 'General Meeting'), ('Weekly_Meeting', 'Weekly Meeting'), ('Late', 'Late'), ('Uniform', 'Uniform'), ('Minimum_Savings', 'Minimum Savings')], max_length=255, null=True),
        ),
    ]
