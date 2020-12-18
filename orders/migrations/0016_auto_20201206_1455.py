# Generated by Django 3.1.3 on 2020-12-06 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20201206_1307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moveorder',
            options={'ordering': ['date_of_confirm'], 'permissions': (('confirm_move_order', 'Потдверждать заказ на переезд'), ('cancel_move_order', 'Отмена заказа на переезд')), 'verbose_name': 'Заказ на переезд', 'verbose_name_plural': 'Заказы на переезд'},
        ),
        migrations.AlterModelOptions(
            name='moverequest',
            options={'permissions': (('rejection_move_request', 'Откланять заявку на переезд'),), 'verbose_name': 'Заявка на переезд', 'verbose_name_plural': 'Заявки на переезд'},
        ),
    ]