# Generated by Django 2.2.12 on 2021-10-21 15:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_geohasharea_metadata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geohasharea',
            name='summary',
        ),
        migrations.AddField(
            model_name='geohasharea',
            name='agg_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Aggregated data for each time range and each category', null=True),
        ),
        migrations.AddField(
            model_name='geohasharea',
            name='agg_status',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Aggregated status for each time range and each category', null=True),
        ),
        migrations.AlterField(
            model_name='geohasharea',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Moving average data for each time_range and each metric', null=True),
        ),
        migrations.AlterField(
            model_name='geohasharea',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Metadata for each metric', null=True),
        ),
        migrations.AlterField(
            model_name='geohasharea',
            name='status',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Status for each time range and each metric', null=True),
        ),
    ]