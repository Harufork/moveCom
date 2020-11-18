# Generated by Django 3.1.3 on 2020-11-18 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moveorder',
            name='confirm_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='confirmed_move_request', to='users.employee', verbose_name='Проверил и потвердил заявку'),
        ),
        migrations.AddField(
            model_name='moveorder',
            name='move_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='move_order', to='orders.moverequest', verbose_name='Заявка на переезд'),
        ),
        migrations.AddField(
            model_name='moveassistancerequest',
            name='confirm_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.employee', verbose_name='Проверил и потвердил заявку'),
        ),
        migrations.AddField(
            model_name='moveassistancerequest',
            name='creater',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создал заявку'),
        ),
        migrations.AddField(
            model_name='employeeformove',
            name='employee',
            field=models.ForeignKey(help_text='Выберите сотрудника, который будет выполнять заказ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fulfills_for_move', to='users.employee', verbose_name='Выполняет'),
        ),
        migrations.AddField(
            model_name='employeeformove',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='move_with_role', to='auth.group', verbose_name='Роль'),
        ),
        migrations.AddField(
            model_name='employeeformove',
            name='move_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_for_move', to='orders.moverequest', verbose_name='Заказ на переезд'),
        ),
        migrations.AddField(
            model_name='assistantformarequest',
            name='employee',
            field=models.ForeignKey(help_text='Выберите сотрудника, который будет выполнять заявку', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fulfills_for_ma_request', to='users.employee', verbose_name='Выполняет'),
        ),
        migrations.AddField(
            model_name='assistantformarequest',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_for_ma_request', to='auth.group', verbose_name='Роль'),
        ),
        migrations.AddField(
            model_name='assistantformarequest',
            name='move_assistance_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assistant_for_request', to='orders.moveassistancerequest', verbose_name='Заявка'),
        ),
    ]
