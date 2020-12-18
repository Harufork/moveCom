# Generated by Django 3.1.3 on 2020-12-05 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('transport', '0002_auto_20201127_1826'),
        ('orders', '0006_auto_20201129_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportForMoveRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('rental_hours', models.PositiveSmallIntegerField(verbose_name='Количество часов аренды')),
                ('mode_transport', models.ForeignKey(help_text='Выберите вид транспорта, который необходим для выполнения заказа', null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.modetransport', verbose_name='Вид транспорта')),
                ('move_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.moverequest', verbose_name='Заказ на переезд')),
            ],
            options={
                'verbose_name': 'Выбор клиентом транспорта на переезд',
                'verbose_name_plural': 'Выбор клиентами транспорта на переезд',
                'ordering': ['move_request'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeForMoveRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('hired_hours', models.PositiveSmallIntegerField(verbose_name='Количество часов найма')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group', verbose_name='Роль')),
                ('move_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.moverequest', verbose_name='Заказ на переезд')),
            ],
            options={
                'verbose_name': 'Выбранная роль клиентом на переезд',
                'verbose_name_plural': 'Выбранные роли клиентом на переезд',
                'ordering': ['move_request'],
            },
        ),
    ]