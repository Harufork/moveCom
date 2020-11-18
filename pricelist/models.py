from django.db import models
from transport.models import ModeTransport
from packing.models import Packing
from django.contrib.auth.models import Group
from users.models import Employee


class PriceListBase(models.Model):
    """Базава модель для прайс листа"""

    class Meta:
        abstract = True
        ordering = ["date_of_creation"]

    total_cost = models.DecimalField(decimal_places=2, max_digits=12,
                                     verbose_name="Стоимость")
    creater = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                verbose_name="Установил цену", null=True,
                                editable=False)
    date_of_creation = models.DateTimeField(verbose_name="Дата создания цены",
                                            auto_now_add=True)
    effective_date = models.DateTimeField(verbose_name="Дата вступления в силу")


class PriceListRole(PriceListBase):
    group = models.OneToOneField(Group, on_delete=models.CASCADE,
                                 verbose_name="Группа")

    class Meta:
        verbose_name = "Прайс-лист часа найма работников"
        verbose_name_plural = "Прайс-лист часа найма работников"

    def __str__(self):
        return f"{format(self.effective_date)}: {self.group} - {self.total_cost}р"


class PriceListModeTransport(PriceListBase):
    mode_transport = models.OneToOneField(ModeTransport, on_delete=models.CASCADE,
                                          verbose_name="Группа")

    class Meta:
        verbose_name = "Прайс-лист часа аренды транспорта"
        verbose_name_plural = "Прайс-лист часа аренды транспорта"

    def __str__(self):
        return f"{format(self.effective_date)}: {self.mode_transport} - {self.total_cost}р"


class PriceListModeTDistance(PriceListBase):
    mode_transport = models.OneToOneField(ModeTransport, on_delete=models.CASCADE,
                                          verbose_name="Группа")

    class Meta:
        verbose_name = "Прайс-лист одного пройденого километра транспортом"
        verbose_name_plural = "Прайс-лист одного пройденого километра транспортом"

    def __str__(self):
        return f"{format(self.effective_date)}: {self.mode_transport} - {self.total_cost}р"


class PriceListPacking(PriceListBase):
    packing = models.OneToOneField(Packing, on_delete=models.CASCADE,
                                   verbose_name="Группа")

    class Meta:
        verbose_name = "Прайс-лист единицы упаковочного материала"
        verbose_name_plural = "Прайс-лист единицы упаковочного материала"

    def __str__(self):
        return f"{format(self.effective_date)}: {self.packing} - {self.total_cost}р"
