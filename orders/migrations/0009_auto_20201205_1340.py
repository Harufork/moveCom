# Generated by Django 3.1.3 on 2020-12-05 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('orders', '0008_auto_20201205_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moveorder',
            name='confirm_request',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='confirmed_move_request', to='users.employee', verbose_name='Проверил и потвердил заявку'),
        ),
    ]
