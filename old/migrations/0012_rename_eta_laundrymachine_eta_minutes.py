# Generated by Django 4.2.3 on 2023-11-14 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('old', '0011_laundrymachine_eta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laundrymachine',
            old_name='eta',
            new_name='eta_minutes',
        ),
    ]
