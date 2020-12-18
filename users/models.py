from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from config.settings import DATETIME_FORMAT
from django.urls import reverse


class Profile(models.Model):
    """Дополнительная информация для пользователей"""
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name="Пользователь")
    patronymic = models.CharField(max_length=30,
                                  verbose_name="Отчество",
                                  blank=True)
    phone_number = models.CharField(max_length=20,
                                    verbose_name="Номер телефона")
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["user"]  # сортировка при выводе
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        try:
            patronymic = " " + self.user.profile.patronymic
        except Profile.DoesNotExist:
            patronymic = ""
        return f"{self.user.first_name} {self.user.last_name}" \
               f" {self.patronymic}"

    def get_absolute_url(self):
        return reverse('profile', args=[self.pk])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля для пользователя при его создании"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """Изменение профиля при изменении пользователя"""
    if not created:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            pass


class Employee(models.Model):
    """Таблица для дополнительной информации для сотрудников, а также
    для уменьшение задержки поиска сотрудников в базе, при их выборе на заказ"""
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name="Пользователь")
    available = models.BooleanField(verbose_name="Активен", default=False,
                                  help_text="Является ли сотрудник активным "
                                            "для работы с заказами")

    class Meta:
        ordering = ["user"]  # сортировка при выводе
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            try:
                patronymic = " " + self.user.profile.patronymic
            except Profile.DoesNotExist:
                patronymic = ""

            return f"{'Активен' if self.available else 'Не активен'}: " \
                   f"{self.user.first_name} {self.user.last_name}" \
                   f"{patronymic}"
        else:
            return f"{'Активен' if self.available else 'Не активен'}: {self.user.get_username()}"

    def get_absolute_url(self):
        return reverse('employee', args=[self.pk])


@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    """Создание профиля сотрудника для пользователя при его создании"""
    if created and instance.is_staff:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_employee(sender, instance, created, **kwargs):
    """Изменение профиля сотрудника при изменении пользователя"""
    if not created and instance.is_staff:
        try:
            instance.employee.save()
        except Employee.DoesNotExist:
            Employee.objects.create(user=instance)


class EmployeeRole(models.Model):
    """Дополнительная информация для group"""
    group = models.OneToOneField(Group, on_delete=models.CASCADE,
                                 verbose_name="Группа")
    image = models.ImageField(upload_to="static/image/data/employeerole",
                              verbose_name="Изображение",
                              blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    available = models.BooleanField(verbose_name="Активна", default=False)
    available_in_order = models.BooleanField(verbose_name="Найм в заказе на переезд", default=False,
                                           help_text="Доступен для найма клиентом в заказе на переезд")
    available_in_request = models.BooleanField(verbose_name="Найм в заявке на помощь", default=False,
                                             help_text="Участвует в заявке помощи с заказом")

    class Meta:
        ordering = ["group"]  # сортировка при выводе
        verbose_name = "Роль сотрудника"
        verbose_name_plural = "Роли сотрудников"

    def __str__(self):
        return self.group.name

    def get_absolute_url(self):
        return reverse('employeerole', args=[self.pk])


class Notification(models.Model):
    """Уведомления для пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="Пользователь", related_name="notification")
    date_of_creation = models.DateTimeField(verbose_name="Дата создания заказа",
                                            auto_now_add=True)
    content = models.TextField(verbose_name="Содержание")
    viewed = models.BooleanField(verbose_name="Просмотрено", default=False)

    class Meta:
        ordering = ["viewed", "-date_of_creation"]  # сортировка при выводе
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"{format(self.date_of_creation, DATETIME_FORMAT)} - {self.user}: {self.content}"

    def get_absolute_url(self):
        return reverse('notification', args=[self.pk])