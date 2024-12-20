# Generated by Django 5.1.1 on 2024-11-05 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_planner', '0006_restaurant_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='image',
            field=models.ImageField(upload_to='images/activity'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='image',
            field=models.ImageField(upload_to='images/hotel'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/restaurant'),
        ),
    ]
