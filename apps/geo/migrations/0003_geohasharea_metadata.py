# Generated by Django 2.2.12 on 2021-10-19 13:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20211017_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='geohasharea',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Metadata', null=True),
        ),
    ]
