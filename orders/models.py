from django.db import models
from django.contrib.auth.models import User
from users.models import Employee
from config.settings import DATETIME_FORMAT
from django.contrib.auth.models import Group
from transport.models import Transport, ModeTransport
from packing.models import Packing
from django.urls import reverse
from pricelist.models import PriceRole, PriceModeTransport, PriceModeTDistance, PricePacking
import datetime


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
    phone_number = models.CharField(max_length=18,
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
                                 verbose_name="Время приезда")
    date_of_completion = models.DateField(verbose_name="Дата приезда")
    time_of_completion = models.TimeField(verbose_name="Точное время приезда", null=True, blank=True)
    comment = models.TextField(verbose_name="Комментарий пользователя", blank=True,
                               help_text="Введите примечания по заказу")

    def set_status(self, st):
        self.status = st
        self.save()

    def is_confirm(self):
        st = self.status
        if st == 'con' or st == 'ipr' or st == 'com':
            return True
        return False

    def is_in_progress(self):
        if self.status == 'ipr':
            return True
        return False

    def is_completed(self):
        if self.status == 'com':
            return True
        return False

    def is_canceled(self):
        st = self.status
        if st == 'can' or st == 'rej':
            return True
        return False


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

    def get_absolute_url(self):
        return reverse('moveassistancerequest', args=[self.pk])


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

    def get_absolute_url(self):
        return reverse('assistantformarequest', args=[self.pk])


class MoveRequest(RequestBase):
    """Описание заявки на переезд"""
    PAYMENT_TYPE = (
        ('c', 'Наличный рассчет при выполнении заказа'),
        ('n', 'Безналичный рассчет'),
    )
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPE,
                                    default='c', verbose_name="Тип опплаты")
    RECEIVING_PACKING = (
        ('p', 'Самовывозом'),
        ('g', 'При выполнение заказа'),
    )
    receiving_packaging = models.CharField(max_length=1, choices=RECEIVING_PACKING, default='p',
                                           verbose_name="Получение упаковки")

    class Meta:
        verbose_name = "Заявка на переезд"
        verbose_name_plural = "Заявки на переезд"
        permissions = (
            ("rejection_move_request", "Откланять заявку на переезд"),
            ("in_progress_move_request", "Выполнить заказ"),
            ("completed_move_request", "Завершить заказ"),
        )

    def __str__(self):
        return f"{format(self.date_of_creation, DATETIME_FORMAT)}:" \
               f" {self.full_name}"

    def get_absolute_url(self):
        return reverse('moverequest', args=[self.pk])

    def rejection_move_request(self):
        self.status = 'rej'
        self.save()
        if self.move_order is not None:
            self.move_order.delete()


class EmployeeForMoveRequest(models.Model):
    move_request = models.ForeignKey(MoveRequest, on_delete=models.CASCADE,
                                     verbose_name="Заявка на переезд")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name="Роль", null=True)
    total = models.PositiveSmallIntegerField(verbose_name="Количество")
    hired_hours = models.PositiveSmallIntegerField(verbose_name="Количество часов найма")

    class Meta:
        ordering = ["move_request"]
        verbose_name = "Выбранная роль клиентом на переезд"
        verbose_name_plural = "Выбранные роли клиентом на переезд"

    def __str__(self):
        return f"{format(self.move_request)}: {self.group} - {self.total} люд. на {self.hired_hours} ч."

    def get_absolute_url(self):
        return reverse('employeeformoverequest', args=[self.pk])


class TransportForMoveRequest(models.Model):
    move_request = models.ForeignKey(MoveRequest, on_delete=models.CASCADE,
                                     verbose_name="Заявка на переезд")
    mode_transport = models.ForeignKey(ModeTransport, on_delete=models.SET_NULL,
                                       verbose_name="Вид транспорта", null=True,
                                       help_text="Выберите вид транспорта, который"
                                                 " необходим для выполнения заказа")
    total = models.PositiveSmallIntegerField(verbose_name="Количество")
    hired_hours = models.PositiveSmallIntegerField(verbose_name="Количество часов аренды")

    class Meta:
        ordering = ["move_request"]
        verbose_name = "Выбор клиентом транспорта на переезд"
        verbose_name_plural = "Выбор клиентами транспорта на переезд"

    def __str__(self):
        return f"{format(self.move_request)}: {self.mode_transport} - {self.total} шт. на {self.hired_hours}ч."

    def get_absolute_url(self):
        return reverse('transportformoverequest', args=[self.pk])


class MoveOrder(models.Model):
    """Описание заказа на переезд"""
    move_request = models.OneToOneField(MoveRequest, on_delete=models.CASCADE,
                                        verbose_name="Заявка на переезд",
                                        related_name="move_order")
    date_of_confirm = models.DateTimeField(verbose_name="Дата потверждения",
                                           null=True,
                                           editable=False)
    confirm_request = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                        verbose_name="Проверил и потвердил заявку",
                                        null=True, related_name="confirmed_move_request",
                                        editable=False)
    total_cost = models.DecimalField(decimal_places=2, max_digits=12,
                                     verbose_name="Итоговая стоимость заказа")

    # TODO: Добавить комментарии для сотрудников
    class Meta:
        ordering = ["date_of_confirm"]
        verbose_name = "Заказ на переезд"
        verbose_name_plural = "Заказы на переезд"
        permissions = (
            ("confirm_move_order", "Потдверждать заказ на переезд"),
            ("cancel_move_order", "Отмена заказа на переезд"),
            ("in_progress_move_order", "Начать выполнение заказа на переезд"),
            ("completed_move_order", "Завершение заказа на переезд"),
        )

    def __str__(self):
        if self.is_confirm():
            if self.date_of_confirm is not None:
                return f"Подтвержден: {format(self.date_of_confirm, DATETIME_FORMAT)}:" \
                       f" {self.total_cost} - {self.move_request}"
            else:
                return f"Подтвержден: {self.total_cost} - {self.move_request}"
        else:
            return f"Не подтвержден: {self.total_cost} - {self.move_request}"

    def get_absolute_url(self):
        return reverse('moveorder', args=[self.pk])

    # Я понимаю, что для объекта стоило использовать булева для быстродействия поиска,
    # но так как это курсач пуска будет так
    def is_confirm(self):
        st = self.move_request.status
        if st == 'con' or st == 'ipr' or st == 'com':
            return True
        return False

    def is_completed(self):
        if self.move_request.status == 'com':
            return True
        return False

    def is_in_progress(self):
        if self.move_request.status == 'ipr':
            return True
        return False

    def is_canceled(self):
        st = self.move_request.status
        if st == 'can' or st == 'rej':
            return True
        return False

    def confirm_move_order(self, employee):
        self.move_request.set_status('con')
        self.date_of_confirm = datetime.datetime.now()
        self.confirm_request = employee
        self.save()

    def cancel_move_order(self):
        self.move_request.set_status('can')

    def in_progress_move_order(self):
        self.move_request.set_status('ipr')

    def completed_move_order(self):
        self.move_request.set_status('com')

    def calculate_total_cost(self):
        # Маршруты
        total_cost = 0
        total_distance = 0
        for obj in RouteMove.objects.filter(move_request=self.move_request):
            total_distance += obj.distance
        # Транспорт
        # Чтобы множество раз не искать прайс-лист для одинаковых объектов
        price_mt = None
        price_mtd = None
        for obj in TransportForMove.objects.filter(move_order=self):
            if price_mt is not None:
                if price_mt.mode_transport == obj.mode_transport:
                    total_cost += obj.hired_hours * price_mt.cost
                if price_mtd is not None:
                    total_cost += total_distance * price_mtd.cost
                continue
            price_mt = PriceModeTransport.objects.filter(mode_transport=obj.mode_transport,
                                                         effective_date__lte=datetime.datetime.now()).first()
            if price_mt is not None:
                total_cost += obj.hired_hours * price_mt.cost

            price_mtd = PriceModeTDistance.objects.filter(mode_transport=obj.mode_transport,
                                                          effective_date__lte=datetime.datetime.now()).first()
            if price_mtd is not None:
                total_cost += total_distance * price_mtd.cost
        del price_mt
        del price_mtd
        del total_distance
        # Упаковка
        for obj in PackingForMove.objects.filter(move_request=self.move_request):
            price = PricePacking.objects.filter(packing=obj.packing,
                                                effective_date__lte=datetime.datetime.now()).first()
            if price is not None:
                total_cost += obj.total * price.cost
        # Персонал
        price = None
        for obj in EmployeeForMove.objects.filter(move_order=self):
            if price is not None:
                if price.group == obj.group:
                    total_cost += obj.hired_hours * price.cost
                    continue
            price = PriceRole.objects.filter(group=obj.group,
                                             effective_date__lte=datetime.datetime.now()).first()
            if price is not None:
                total_cost += obj.hired_hours * price.cost

        self.total_cost = total_cost
        self.save()


class EmployeeForMove(models.Model):
    """Описание выбора людей для выполнения переезда"""
    move_order = models.ForeignKey(MoveOrder, on_delete=models.CASCADE,
                                   verbose_name="Заказ на переезд")
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
        ordering = ["move_order"]
        verbose_name = "Выбор сотрудника на выполнение переезда"
        verbose_name_plural = "Выбор сотрудников на выполнение переезда"

    def __str__(self):
        return f"{format(self.move_order)}: {self.group} - {self.employee}"

    def get_absolute_url(self):
        return reverse('employeeformove', args=[self.pk])


class TransportForMove(models.Model):
    """Описание выбора транспорта для выполнения переезда"""
    move_order = models.ForeignKey(MoveOrder, on_delete=models.CASCADE,
                                   verbose_name="Заказ на переезд")
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
    hired_hours = models.PositiveSmallIntegerField(verbose_name="Количество часов аренды")

    class Meta:
        ordering = ["move_order"]
        verbose_name = "Выбор транспорта на выполнение переезда"
        verbose_name_plural = "Выбор транспорта на выполнение переезда"

    def __str__(self):
        return f"{format(self.move_order)}: {self.mode_transport} - {self.transport}"

    def get_absolute_url(self):
        return reverse('transportformove', args=[self.pk])


class PackingForMove(models.Model):
    """Описание выбора транспорта для выполнения переезда"""
    move_request = models.ForeignKey(MoveRequest, on_delete=models.CASCADE,
                                     verbose_name="Заявка на переезд",
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

    def get_absolute_url(self):
        return reverse('packingformove', args=[self.pk])


class RouteMove(models.Model):
    """Описание маршрута"""
    move_request = models.ForeignKey(MoveRequest, on_delete=models.CASCADE,
                                     verbose_name="Заявка на переезд",
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

    def get_absolute_url(self):
        return reverse('routemove', args=[self.pk])
