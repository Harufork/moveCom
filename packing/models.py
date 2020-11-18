from django.db import models


class TypePacking(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Наименование типа упаковки",
                            help_text="Введите наименование типа упаковки")

    class Meta:
        ordering = ["name"]  # сортировка при выводе
        verbose_name = "Тип упаковки"
        verbose_name_plural = "Типы упаковки"

    def __str__(self):
        return self.name


class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Наименование единицы измерения",
                            help_text="Введите наименование единицы измерения")
    symbol = models.CharField(max_length=10,
                              verbose_name="Обозначение единицы измерения",
                              help_text="Введите обозначение единицы измерения")

    class Meta:
        ordering = ["name"]  # сортировка при выводе
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"

    def __str__(self):
        return self.symbol


class Packing(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Наименование упаковки",
                            help_text="Введите наименование упаковочного материала")
    aviable = models.BooleanField(verbose_name="Доступность упаковки",
                                  help_text="Выберите доступен ли упаковочный материал",
                                  default=False)
    description = models.TextField(verbose_name="Описание упаковки",
                                   help_text="Введите краткое описание и предназначение "
                                             "упаковочного материала")
    image = models.ImageField(upload_to="static/image",
                              verbose_name="Изображение упаковки")
    type = models.ForeignKey(TypePacking, on_delete=models.SET_NULL, null=True,
                             blank=True, verbose_name="Тип упаковки",
                             help_text="Выберите тип упаковки")
    unit = models.ForeignKey(UnitOfMeasurement, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             verbose_name="Единица измерения",
                             help_text="Выберите единицу измерений")

    class Meta:
        ordering = ["name"]  # сортировка при выводе
        verbose_name = "Упаковочный материал"
        verbose_name_plural = "Упаковочный материал"

    def __str__(self):
        return self.name
