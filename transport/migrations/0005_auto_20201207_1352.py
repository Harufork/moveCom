# Generated by Django 3.1.3 on 2020-12-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0004_modetransport_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modetransport',
            name='image',
            field=models.ImageField(blank=True, default=0, upload_to='static/image/data/transport', verbose_name='Изображение вида'),
            preserve_default=False,
        ),
    ]