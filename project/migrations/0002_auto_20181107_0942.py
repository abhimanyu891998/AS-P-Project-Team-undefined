# Generated by Django 2.1.2 on 2018-11-07 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliniclocation',
            old_name='latitute',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='cliniclocation',
            old_name='longitute',
            new_name='longitude',
        ),
        migrations.RenameField(
            model_name='hospitallocation',
            old_name='latitute',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='hospitallocation',
            old_name='longitute',
            new_name='longitude',
        ),
    ]