from django.db import models
from django.urls import reverse


class TypePacking(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Наименование",
                            help_text="Введите наименование типа упаковки",
                            unique=True)
    available = models.BooleanField(verbose_name="Доступен",
                                    help_text="Выберите доступен ли тип упаковки для выбора клиентом",
                                    default=False)

    class Meta:
        ordering = ["name"]  # сортировка при выводе
        verbose_name = "Тип упаковки"
        verbose_name_plural = "Типы упаковки"
        # permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Формирование ссылки на просмотр объекта.
        Также добавляется соответсвующая кнопка в admin"""
        return reverse('typepacking', args=[self.pk])



class Measurement(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Наименование",
                            help_text="Введите наименование единицы измерения",
                            unique=True)
    symbol = models.CharField(max_length=10,
                              verbose_name="Обозначение",
                              help_text="Введите обозначение единицы измерения",
                              unique=True)

    class Meta:
        ordering = ["name"]  # сортировка при выводе
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"

    def __str__(self):
        return self.symbol

    def get_absolute_url(self):
        return reverse('measurement', args=[self.pk])




class Packing(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Наименование упаковки",
                            help_text="Введите наименование упаковочного материала",
                            unique=True)
    available = models.BooleanField(verbose_name="Доступность упаковки",
                                  help_text="Выберите доступен ли упаковочный материал",
                                  default=False)
    description = models.TextField(verbose_name="Описание упаковки", blank=True,
                                   help_text="Введите краткое описание и предназначение "
                                             "упаковочного материала")
    image = models.ImageField(upload_to="static/image/data/packing",
                              verbose_name="Изображение упаковки",
                              blank=True)
    type = models.ForeignKey(TypePacking, on_delete=models.SET_NULL, null=True,
                             blank=True, verbose_name="Тип упаковки",
                             help_text="Выберите тип упаковки")
    unit = models.ForeignKey(Measurement, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             verbose_name="Единица измерения",
                             help_text="Выберите единицу измерений")

    class Meta:
        ordering = ["name"]  # сортировка при выводе
        verbose_name = "Упаковочный материал"
        verbose_name_plural = "Упаковочные материалы"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('packing', args=[self.pk])

# TODO: Добавить при удалении объекта удаление и картинки