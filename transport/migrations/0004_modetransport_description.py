# Generated by Django 3.1.3 on 2020-12-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0003_auto_20201207_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='modetransport',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
