# Generated by Django 4.2.3 on 2023-10-24 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('old', '0008_discordhook_ping_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='discordhook',
            name='avatar_url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='discordhook',
            name='message_id',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
