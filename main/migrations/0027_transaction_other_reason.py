# Generated by Django 3.2 on 2022-09-25 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20220925_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='other_reason',
            field=models.TextField(default='This is a test value'),
            preserve_default=False,
        ),
    ]