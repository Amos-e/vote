# Generated by Django 3.2 on 2022-12-05 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_auto_20221205_1637'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tulinaawe',
            options={'ordering': ['-date_due'], 'verbose_name_plural': 'Tulinaawe'},
        ),
    ]
