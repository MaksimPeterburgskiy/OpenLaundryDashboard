# Generated by Django 4.2.3 on 2023-10-10 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('old', '0005_discordhook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discordhook',
            name='machine',
        ),
        migrations.AddField(
            model_name='discordhook',
            name='machines',
            field=models.ManyToManyField(to='old.laundrymachine'),
        ),
    ]