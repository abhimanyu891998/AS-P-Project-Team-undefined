# Generated by Django 2.1.2 on 2018-11-07 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20181107_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
    ]
