# Generated by Django 3.2 on 2022-08-26 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_tulinaawe_tulinaawecontributor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.member')),
            ],
        ),
        migrations.AlterModelOptions(
            name='tulinaawe',
            options={'verbose_name_plural': 'Tulinaawe'},
        ),
        migrations.CreateModel(
            name='LoanPayment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('payment', models.IntegerField(default=0)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.loan')),
            ],
        ),
    ]
