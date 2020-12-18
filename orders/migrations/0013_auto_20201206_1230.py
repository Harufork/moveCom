# Generated by Django 3.1.3 on 2020-12-06 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_moveorder_isconfirm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeformoverequest',
            name='move_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.moverequest', verbose_name='Заявка на переезд'),
        ),
        migrations.AlterField(
            model_name='transportformoverequest',
            name='move_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.moverequest', verbose_name='Заявка на переезд'),
        ),
    ]
