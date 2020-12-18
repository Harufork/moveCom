# Generated by Django 3.1.3 on 2020-12-11 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_auto_20201207_1346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moveorder',
            options={'ordering': ['date_of_confirm'], 'permissions': (('confirm_move_order', 'Потдверждать заказ на переезд'), ('cancel_move_order', 'Отмена заказа на переезд'), ('in_progress_move_order', 'Начать выполнение заказа на переезд'), ('completed_move_order', 'Завершение заказа на переезд')), 'verbose_name': 'Заказ на переезд', 'verbose_name_plural': 'Заказы на переезд'},
        ),
        migrations.AlterModelOptions(
            name='moverequest',
            options={'permissions': (('rejection_move_request', 'Откланять заявку на переезд'), ('in_progress_move_request', 'Выполнить заказ'), ('completed_move_request', 'Завершить заказ')), 'verbose_name': 'Заявка на переезд', 'verbose_name_plural': 'Заявки на переезд'},
        ),
        migrations.AlterField(
            model_name='moveassistancerequest',
            name='comment',
            field=models.TextField(blank=True, help_text='Введите примечания по заказу', verbose_name='Комментарий пользователя'),
        ),
        migrations.AlterField(
            model_name='moverequest',
            name='comment',
            field=models.TextField(blank=True, help_text='Введите примечания по заказу', verbose_name='Комментарий пользователя'),
        ),
    ]
