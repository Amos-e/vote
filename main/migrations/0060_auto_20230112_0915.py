# Generated by Django 3.2 on 2023-01-12 06:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0059_alter_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='admitted_by_1',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='admitted_by_2',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='amount_in_words',
            field=models.CharField(default='Zero', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='box_no',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='business_address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='business_location',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='business_monthly_income',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='business_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='business_sector',
            field=models.CharField(blank=True, choices=[('transport', 'Transport'), ('hospitality', 'Hospitality'), ('real_estate', 'Real Estate'), ('tourism', 'Tourism'), ('wholesale_retail', 'Wholesale / Retail'), ('financial_services', 'Financial Services'), ('health_care', 'Health Care'), ('manufacturing', 'Manufacturing'), ('education', 'Education')], max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='business_sector_others',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='data_captured_by',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='data_date_capture',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='effective_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='member',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='identication_no',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='marital_status',
            field=models.CharField(choices=[('single', 'Single'), ('married', 'Married')], default='single', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='memberbership_approved_by',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='mode_of_remittance',
            field=models.CharField(blank=True, choices=[('check_off', 'Check Off'), ('direct_deposit', 'Direct Deposit'), ('standing_order', 'Standing Order'), ('pay_bill_m_money', 'Paybill (M-Money)')], max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='proposed_monthly_contribution',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='residence',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='source_of_income',
            field=models.CharField(blank=True, choices=[('salary', 'Salary'), ('business', 'Business'), ('pension', 'Pension')], max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='system_approval_by',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='town',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='town_code',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='NominessForDeposits',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('id_no', models.CharField(max_length=255)),
                ('percentage', models.PositiveIntegerField(default=0)),
                ('date_of_birth', models.DateTimeField()),
                ('mobile_no', models.CharField(max_length=255)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.member')),
            ],
        ),
    ]
