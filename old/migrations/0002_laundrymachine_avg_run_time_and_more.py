# Generated by Django 4.2.3 on 2023-10-03 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('old', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='laundrymachine',
            name='avg_run_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='laundrymachine',
            name='last_current',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='laundrymachine',
            name='last_end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='laundrymachine',
            name='last_power',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='laundrymachine',
            name='last_start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='laundrymachine',
            name='last_voltage',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='laundrymachine',
            name='on_power_threshold',
            field=models.IntegerField(default=0),
        ),
    ]
