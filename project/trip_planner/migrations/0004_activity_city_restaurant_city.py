# Generated by Django 5.1.1 on 2024-11-04 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_planner', '0003_rename_arrival_date_flight_arrival_date_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='city',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='city',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
