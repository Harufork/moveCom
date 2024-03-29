# Generated by Django 3.1.3 on 2020-11-27 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование единицы измерения', max_length=255, unique=True, verbose_name='Наименование')),
                ('symbol', models.CharField(help_text='Введите обозначение единицы измерения', max_length=10, unique=True, verbose_name='Обозначение')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TypePacking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование типа упаковки', max_length=255, unique=True, verbose_name='Наименование')),
                ('available', models.BooleanField(default=False, help_text='Выберите доступен ли тип упаковки для выбора клиентом', verbose_name='Доступен')),
            ],
            options={
                'verbose_name': 'Тип упаковки',
                'verbose_name_plural': 'Типы упаковки',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Packing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование упаковочного материала', max_length=255, unique=True, verbose_name='Наименование упаковки')),
                ('available', models.BooleanField(default=False, help_text='Выберите доступен ли упаковочный материал', verbose_name='Доступность упаковки')),
                ('description', models.TextField(blank=True, help_text='Введите краткое описание и предназначение упаковочного материала', verbose_name='Описание упаковки')),
                ('image', models.ImageField(blank=True, upload_to='static/image/data/packing', verbose_name='Изображение упаковки')),
                ('type', models.ForeignKey(blank=True, help_text='Выберите тип упаковки', null=True, on_delete=django.db.models.deletion.SET_NULL, to='packing.typepacking', verbose_name='Тип упаковки')),
                ('unit', models.ForeignKey(blank=True, help_text='Выберите единицу измерений', null=True, on_delete=django.db.models.deletion.SET_NULL, to='packing.measurement', verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Упаковочный материал',
                'verbose_name_plural': 'Упаковочные материалы',
                'ordering': ['name'],
            },
        ),
    ]
