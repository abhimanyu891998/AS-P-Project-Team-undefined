# Generated by Django 2.1.2 on 2018-11-06 09:34

import datetime
from django.db import migrations, models
import project.models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_order_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=project.models.image_path),
        ),
        migrations.AddField(
            model_name='order',
            name='dateDelivered',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='dateDispatched',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='dateOrdered',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='order',
            name='dateProcessed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
