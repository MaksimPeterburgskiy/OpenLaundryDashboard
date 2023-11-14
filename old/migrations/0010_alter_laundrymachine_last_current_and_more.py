# Generated by Django 4.2.3 on 2023-11-14 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('old', '0009_discordhook_avatar_url_discordhook_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundrymachine',
            name='last_current',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='laundrymachine',
            name='last_power',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='laundrymachine',
            name='last_voltage',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
    ]