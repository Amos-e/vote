# Generated by Django 3.2 on 2022-08-26 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_transaction_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general', models.BooleanField(default=False)),
                ('withdraw', models.BooleanField(default=False)),
                ('fined', models.BooleanField(default=False)),
                ('savings_to_shares', models.BooleanField(default=False)),
                ('paid_fines', models.BooleanField(default=False)),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.transaction')),
            ],
        ),
    ]
