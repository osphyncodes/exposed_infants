# Generated by Django 5.2.4 on 2025-07-16 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0012_alter_child_agrees_to_fup_alter_child_guardian_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='htssample',
            name='reason',
            field=models.CharField(blank=True, choices=[('DBS_6wks_Ini', 'DBS 6 Weeks Initial'), ('DBS_6wks_Con', 'DBS 6 Weeks Confirmatory'), ('DBS_Rapid_Conf', 'DBS Rapid Confirmatory'), ('Rapid_1yr', 'Rapid @ 1yr'), ('Rapid_2yr', 'Rapid @ 2yr')], max_length=30, null=True),
        ),
    ]
