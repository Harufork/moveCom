# Generated by Django 3.1.3 on 2020-12-05 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20201205_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportformove',
            old_name='rental_hours',
            new_name='hired_hours',
        ),
        migrations.RenameField(
            model_name='transportformoverequest',
            old_name='rental_hours',
            new_name='hired_hours',
        ),
    ]
