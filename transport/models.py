from django.db import models


class ModeTransport(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Наименование вида",
                            help_text="Введите наименование вида (прим. Грузовик 14 т.)")

    class Meta:
        ordering = ["name"]  # сортировка при выводе
        verbose_name = "Вид транспорта"
        verbose_name_plural = "Виды транспорта"

    def __str__(self):
        return self.name


class Transport(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Бренд и модель",
                            help_text="Введите бренд и модель транспорта")
    license_plate = models.CharField(max_length=9,
                                     verbose_name="Гос. номер",
                                     help_text="Введите государственный номер транспорта",
                                     unique=True)
    aviable = models.BooleanField(verbose_name="Активно",
                                  help_text="Выберите доступен ли транспорт сейчас (прим. он"
                                            " может быть в автомастерской)",
                                  default=False)
    mode = models.ForeignKey(ModeTransport, on_delete=models.SET_NULL, null=True,
                             blank=True, verbose_name="Вид авто", help_text="Выберите вид авто")

    class Meta:
        ordering = ["name"]  # сортировка при выводе
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорт"

    def __str__(self):
        return f"{self.name}: {self.license_plate}"
