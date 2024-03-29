# Generated by Django 3.1.3 on 2020-11-27 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModeTransport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование вида (прим. Грузовик 14 т.)', max_length=255, unique=True, verbose_name='Наименование вида')),
                ('image', models.ImageField(upload_to='static/image/data/transport', verbose_name='Изображение вида')),
                ('available', models.BooleanField(default=False, help_text='Выберите доступен ли вид транспорта для выбора', verbose_name='Доступен')),
            ],
            options={
                'verbose_name': 'Вид транспорта',
                'verbose_name_plural': 'Виды транспорта',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите бренд и модель транспорта', max_length=255, verbose_name='Бренд и модель')),
                ('license_plate', models.CharField(help_text='Введите государственный номер транспорта', max_length=9, unique=True, verbose_name='Гос. номер')),
                ('available', models.BooleanField(default=False, help_text='Выберите доступен ли транспорт сейчас (прим. он может быть в автомастерской)', verbose_name='Активно')),
                ('mode', models.ForeignKey(blank=True, help_text='Выберите вид авто', null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport.modetransport', verbose_name='Вид авто')),
            ],
            options={
                'verbose_name': 'Транспорт',
                'verbose_name_plural': 'Транспорт',
                'ordering': ['name'],
            },
        ),
    ]
