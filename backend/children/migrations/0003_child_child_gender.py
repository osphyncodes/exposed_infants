# Generated by Django 5.2.4 on 2025-07-05 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0002_alter_child_child_name_alter_child_guardian_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='child_gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=6),
            preserve_default=False,
        ),
    ]
