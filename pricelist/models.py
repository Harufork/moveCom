from django.db import models
from transport.models import ModeTransport
from packing.models import Packing
from django.contrib.auth.models import Group
from users.models import Employee
from django.urls import reverse

class PriceBase(models.Model):
    """Базава модель для прайс листа"""

    class Meta:
        abstract = True
        ordering = ["-effective_date", "-date_of_creation"]

    cost = models.DecimalField(decimal_places=2, max_digits=12,
                                     verbose_name="Стоимость")
    creater = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                verbose_name="Установил цену", null=True,
                                editable=False)
    date_of_creation = models.DateTimeField(verbose_name="Дата создания цены",
                                            auto_now_add=True)
    effective_date = models.DateTimeField(verbose_name="Дата вступления в силу")



class PriceRole(PriceBase):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                                 verbose_name="Группа")

    class Meta:
        verbose_name = "Цена часа найма работников"
        verbose_name_plural = "Прайс-лист часа найма работников"
        ordering = ["-effective_date", "-date_of_creation"]

    def __str__(self):
        return f"{format(self.effective_date)}: {self.group} - {self.cost}р"

    def get_absolute_url(self):
        return reverse('pricerole', args=[self.pk])


class PriceModeTransport(PriceBase):
    mode_transport = models.ForeignKey(ModeTransport, on_delete=models.CASCADE,
                                          verbose_name="Вид транспорта")

    class Meta:
        verbose_name = "Цена часа аренды транспорта"
        verbose_name_plural = "Прайс-лист часа аренды транспорта"
        ordering = ["-effective_date", "-date_of_creation"]


    def __str__(self):
        return f"{format(self.effective_date)}: {self.mode_transport} - {self.cost}р"

    def get_absolute_url(self):
        return reverse('pricemodetransport', args=[self.pk])


class PriceModeTDistance(PriceBase):
    mode_transport = models.ForeignKey(ModeTransport, on_delete=models.CASCADE,
                                          verbose_name="Вид транспорта")

    class Meta:
        verbose_name = "Цена одного пройденого километра транспортом"
        verbose_name_plural = "Прайс-лист одного пройденого километра транспортом"
        ordering = ["-effective_date", "-date_of_creation"]

    def __str__(self):
        return f"{format(self.effective_date)}: {self.mode_transport} - {self.cost}р"

    def get_absolute_url(self):
        return reverse('pricemodetdistance', args=[self.pk])

class PricePacking(PriceBase):
    packing = models.ForeignKey(Packing, on_delete=models.CASCADE,
                                   verbose_name="Упаковочный материал")

    class Meta:
        verbose_name = "Цена единицы упаковочного материала"
        verbose_name_plural = "Прайс-лист единицы упаковочного материала"
        ordering = ["-effective_date", "-date_of_creation"]

    def __str__(self):
        return f"{format(self.effective_date)}: {self.packing} - {self.cost}р"

    def get_absolute_url(self):
        return reverse('pricepacking', args=[self.pk])
