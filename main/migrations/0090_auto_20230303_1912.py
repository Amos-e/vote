# Generated by Django 3.2 on 2023-03-03 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0089_auto_20230211_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_date', models.DateTimeField()),
                ('second_date', models.DateTimeField()),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.settings')),
            ],
        ),
    ]