# Generated by Django 5.2.4 on 2025-07-22 20:20

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arv_number', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10)),
                ('birthdate', models.DateField()),
                ('outcome', models.CharField(choices=[('On antiretrovirals', 'On antiretrovirals'), ('Patient transferred out', 'Patient transferred out')], max_length=50)),
                ('art_start_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LabResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession_number', models.CharField(max_length=20)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('order_date', models.DateField()),
                ('result', models.CharField(blank=True, max_length=255, null=True)),
                ('date_received', models.DateField(blank=True, null=True)),
                ('mode_of_delivery', models.CharField(blank=True, choices=[('Email', 'Email'), ('Portal', 'Portal'), ('Courier', 'Courier'), ('In-person', 'In-person')], max_length=20, null=True)),
                ('test_reason', models.CharField(blank=True, choices=[('Medical examination, routine', 'Routine Examination'), ('Diagnostic test', 'Diagnostic Test'), ('Follow-up', 'Follow-up')], max_length=100, null=True)),
                ('tat_days', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('arv_number', models.ForeignKey(db_column='arv_number', on_delete=django.db.models.deletion.CASCADE, to='pact.patient', to_field='arv_number')),
            ],
            options={
                'db_table': 'lab_results',
            },
        ),
        migrations.CreateModel(
            name='Regimen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=20)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('regimen', models.CharField(blank=True, max_length=5, null=True)),
                ('arv_number', models.ForeignKey(db_column='arv_number', on_delete=django.db.models.deletion.CASCADE, to='pact.patient', to_field='arv_number')),
            ],
            options={
                'db_table': 'regimen',
            },
        ),
    ]
