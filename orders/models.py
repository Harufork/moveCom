from django.db import models
from django.contrib.auth.models import User
from users.models import Employee
from config.settings import DATETIME_FORMAT
from django.contrib.auth.models import Group
from transport.models import Transport, ModeTransport
from packing.models import Packing


class RequestBase(models.Model):
    class Meta:
        abstract = True
        ordering = ["date_of_creation"]

    ORDER_STATUS = (
        ('pen', 'В ожидании рассмотрения'),
        ('con', 'Подтверждёна'),
        ('ipr', 'В процессе выполнения'),
        ('com', 'Завершена'),
        ('can', 'Отменена'),
        ('rej', 'Отклонена'),
    )
    status = models.CharField(max_length=3, choices=ORDER_STATUS, default='pen',
                              verbose_name="Статус заказа",
                              help_text="Выберите статус заказа")
    date_of_creation = models.DateTimeField(verbose_name="Дата создания заявки",
                                            auto_now_add=True)
    creater = models.ForeignKey(User, on_delete=models.SET_NULL,
                                verbose_name="Создал заявку", editable=False,
                                null=True)
    full_name = models.CharField(max_length=255,
                                 verbose_name="ФИО клиента",
                                 help_text="Введите ФИО клиента")
    phone_number = models.CharField(max_length=20,
                                    verbose_name="Номер телефона",
                                    help_text="Введите номер телефона")
    TIME_TYPE = (
        ('m', 'Утром'),
        ('d', 'Днём'),
        ('e', 'Вечером'),
        ('n', 'Ночью'),
        ('o', 'Точное время'),
    )
    time_type = models.CharField(max_length=1, choices=TIME_TYPE, default='m',
                                 verbose_name="Время выполнения заказа")
    date_of_completion = models.DateTimeField(verbose_name="Дата приезда")
    comment = models.TextField(verbose_name="Комментарий", blank=True,
                               help_text="Введите примечания по заказу")


class MoveAssistanceRequest(RequestBase):
    """Описание заявки на помощь с переездом"""
    confirm_request = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                        verbose_name="Проверил и потвердил заявку",
                                        null=True, blank=True)
    client_adress = models.CharField(max_length=20,
                                     verbose_name="Адрес клиента",
                                     help_text="Введите адрес клиента")

    class Meta:
        verbose_name = "Заявка на помощь с переездом"
        verbose_name_plural = "Заявки на помощь с переездом"

    def __str__(self):
        return f"{format(self.date_of_creation, DATETIME_FORMAT)}:" \
               f" {self.full_name} - {self.client_adress}"


class AssistantForMARequest(models.Model):
    """Описание выбора людей для выполнентт заявки на помощь с переездом"""
    move_assistance_request = models.ForeignKey(MoveAssistanceRequest, on_delete=models.CASCADE,
                                                verbose_name="Заявка",
                                                related_name="assistant_for_request")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name="Роль", null=True,
                              related_name="role_for_ma_request")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 verbose_name="Выполняет", null=True,
                                 related_name="fulfills_for_ma_request",
                                 help_text="Выберите сотрудника, который"
                                           " будет выполнять заявку")

    class Meta:
        ordering = ["move_assistance_request"]
        verbose_name = "Выбор сотрудник на помощь с переездом"
        verbose_name_plural = "Выбор сотрудников на помощь с переездом"

    def __str__(self):
        return f"{format(self.move_assistance_request)}: {self.group} - {self.employee}"


class MoveRequest(RequestBase):
    """Описание заявки на переезд"""
    class Meta:
        verbose_name = "Заявка на переезд"
        verbose_name_plural = "Заявки на переезд"

    def __str__(self):
        return f"{format(self.date_of_creation, DATETIME_FORMAT)}:" \
               f" {self.full_name}"


class MoveOrder(models.Model):
    """Описание заказа на переезд"""
    move_request = models.OneToOneField(MoveRequest, on_delete=models.CASCADE,
                                        verbose_name="Заявка на переезд",
                                        related_name="move_order")
    date_of_confirm = models.DateTimeField(verbose_name="Дата потверждения",
                                           auto_now_add=True)
    confirm_request = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                        verbose_name="Проверил и потвердил заявку",
                                        null=True, related_name="confirmed_move_request")
    RECEIVING_PACKING = (
        ('p', 'Самовывоз'),
        ('g', 'Получение при выполнение заказа'),
    )
    receiving_packaging = models.CharField(max_length=1, choices=RECEIVING_PACKING, default='p',
                                           verbose_name="Тип получения упаковки")
    total_cost = models.DecimalField(decimal_places=2, max_digits=12,
                                     verbose_name="Итоговая стоимость заказа")
    PAYMENT_TYPE = (
        ('c', 'Наличный рассчет при выполнении заказа'),
        ('n', 'Безналичный рассчет'),
    )
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE,
                                    default='pen', verbose_name="Тип опплаты")

    class Meta:
        ordering = ["date_of_confirm"]
        verbose_name = "Заказ на переезд"
        verbose_name_plural = "Заказы на переезд"

    def __str__(self):
        return f"{format(self.date_of_confirm, DATETIME_FORMAT)}:" \
               f" {self.total_cost} - {self.move_request}"


class EmployeeForMove(models.Model):
    """Описание выбора людей для выполнения переезда"""
    move_request = models.ForeignKey(MoveRequest, on_delete=models.CASCADE,
                                     verbose_name="Заказ на переезд",
                                     related_name="employee_for_move")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name="Роль", null=True,
                              related_name="move_with_role")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 verbose_name="Выполняет", null=True,
                                 related_name="fulfills_for_move",
                                 help_text="Выберите сотрудника, который"
                                           " будет выполнять заказ")
    hired_hours = models.PositiveSmallIntegerField(verbose_name="Количество часов найма")

    class Meta:
        ordering = ["move_request"]
        verbose_name = "Выбор сотрудника на выполнение переезда"
        verbose_name_plural = "Выбор сотрудников на выполнение переезда"

    def __str__(self):
        return f"{format(self.move_request)}: {self.group} - {self.employee}"


class TransportForMove(models.Model):
    """Описание выбора транспорта для выполнения переезда"""
    move_request = models.ForeignKey(MoveRequest, on_delete=models.CASCADE,
                                     verbose_name="Заказ на переезд",
                                     related_name="transport_for_move")
    mode_transport = models.ForeignKey(ModeTransport, on_delete=models.SET_NULL,
                                       verbose_name="Вид транспорта", null=True,
                                       related_name="move_with_mode_transport",
                                       help_text="Выберите вид транспорта, который"
                                                 " необходим для выполнения заказа")
    transport = models.ForeignKey(Transport, on_delete=models.SET_NULL,
                                  verbose_name="Транспорт", null=True,
                                  related_name="move_with_transport",
                                  help_text="Выберите транспорт, который"
                                            " необходим для выполнения заказа")
    rental_hours = models.PositiveSmallIntegerField(verbose_name="Количество часов аренды")

    class Meta:
        ordering = ["move_request"]
        verbose_name = "Выбор транспорта на выполнение переезда"
        verbose_name_plural = "Выбор транспорта на выполнение переезда"

    def __str__(self):
        return f"{format(self.move_request)}: {self.mode_transport} - {self.transport}"


class PackingForMove(models.Model):
    """Описание выбора транспорта для выполнения переезда"""
    move_request = models.ForeignKey(MoveRequest, on_delete=models.CASCADE,
                                     verbose_name="Заказ на переезд",
                                     related_name="packing_for_move")
    packing = models.ForeignKey(Packing, on_delete=models.SET_NULL,
                                verbose_name="Упаковочный материал", null=True,
                                related_name="move_with_packing")
    total = models.PositiveSmallIntegerField(verbose_name="Количество")

    class Meta:
        ordering = ["move_request"]
        verbose_name = "Выбор упаковочного материала на выполнение переезда"
        verbose_name_plural = "Выбор упаковочного материала на выполнение переезда"

    def __str__(self):
        return f"{format(self.move_request)}: {self.packing} - {self.total}"


class RouteMove(models.Model):
    """Описание маршрута"""
    move_request = models.ForeignKey(MoveRequest, on_delete=models.CASCADE,
                                     verbose_name="Заказ на переезд",
                                     related_name="route_for_move")
    point_a = models.CharField(max_length=255,
                               verbose_name="Адрес погрузки вещей")
    point_b = models.CharField(max_length=255,
                               verbose_name="Адрес разгрузки вещей")
    distance = models.PositiveSmallIntegerField(verbose_name="Дистанция между адресами (в км.)")

    class Meta:
        ordering = ["move_request"]
        verbose_name = "Марщрут переезда"
        verbose_name_plural = "Марщруты переездов"

    def __str__(self):
        return f"{format(self.move_request)}: {self.point_a} - {self.point_b}"
