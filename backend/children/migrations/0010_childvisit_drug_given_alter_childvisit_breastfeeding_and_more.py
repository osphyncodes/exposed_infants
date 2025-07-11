# Generated by Django 5.2.4 on 2025-07-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0009_alter_htssample_date_received_alter_htssample_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='childvisit',
            name='drug_given',
            field=models.CharField(blank=True, choices=[('None', 'No Drugs Given'), ('CPT', 'Cotrimoxazole Prophylaxis (CPT)'), ('NVP', 'Nevirapine (NVP)')], default='CPT', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='childvisit',
            name='breastfeeding',
            field=models.CharField(blank=True, choices=[('Exc', 'Exclusive'), ('M', 'Mixed/Complement'), ('<6', 'Stopped last 6 Weeks'), ('C', 'Stopped over 6w. ago')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='childvisit',
            name='cpt_given',
            field=models.PositiveIntegerField(blank=True, help_text='Number of CPT/NVP tablets given', null=True),
        ),
        migrations.AlterField(
            model_name='childvisit',
            name='infection_status',
            field=models.CharField(blank=True, choices=[('A', 'Not Infected'), ('B', 'Infected'), ('C', 'Not ART Eligible'), ('D', 'PSHD -> ART')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='htssample',
            name='test_type',
            field=models.CharField(choices=[('DBS', 'Dried Blood Spot'), ('Rapid', 'Rapid Test')], max_length=10),
        ),
    ]
