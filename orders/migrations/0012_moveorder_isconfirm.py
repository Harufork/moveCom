# Generated by Django 3.1.3 on 2020-12-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20201205_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='moveorder',
            name='isConfirm',
            field=models.BooleanField(default=False, help_text='Заказ потвержден сотрудником', verbose_name='Заказ потверждён'),
        ),
    ]
