# Generated by Django 3.1.3 on 2020-12-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_employeerole_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerole',
            name='image',
            field=models.ImageField(blank=True, default=0, upload_to='static/image/data/employeerole', verbose_name='Изображение'),
            preserve_default=False,
        ),
    ]
