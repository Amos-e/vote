# Generated by Django 3.2 on 2023-03-04 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0092_financialyear_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='settings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.settings'),
        ),
    ]
