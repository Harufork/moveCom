from django import forms
from django.core.exceptions import ValidationError
from additional_functions import get_verbose_of_field_from_class
from .models import MoveRequest
from django.core.validators import RegexValidator
import datetime


class DateTypeInput(forms.DateInput):
    input_type = 'date'


class TimeTypeInput(forms.TimeInput):
    input_type = 'time'


class PhoneTypeInput(forms.TextInput):
    input_type = 'tel'


class ForClientMoveRequest(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+\d\s\(\d{3}\)\s\d{3}\-\d{2}\-\d{2}$',
                                 message="Введите номер телефона в формате: '+7 (999) 999-99-99'.")
    full_name = forms.CharField(max_length=255, label="Ваше имя и фамилия")
    date_of_completion = forms.DateField(label=get_verbose_of_field_from_class(MoveRequest, 'date_of_completion'),
                                         widget=DateTypeInput())
    time_of_completion = forms.TimeField(label=get_verbose_of_field_from_class(MoveRequest, 'time_of_completion'),
                                         widget=TimeTypeInput(), required=False)
    phone_number = forms.CharField(validators=[phone_regex], max_length=18,
                                   label=get_verbose_of_field_from_class(MoveRequest, 'phone_number'),
                                   widget=PhoneTypeInput(attrs=
                                                         {'class': "mask-phone",
                                                          'pattern': "[+]\d\s[(]\d{3}[)]\s\d{3}[-]\d{2}[-]\d{2}"
                                                          }))

    class Meta:
        model = MoveRequest
        fields = ["time_type","receiving_packaging","payment_type"]

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        full_name = full_name.strip()
        # if full_name.isdigit():
        if any(ch.isdigit() for ch in full_name):
            raise ValidationError("Фамилия или имя не должны содержать цифры.")
        return full_name

    def clean_date_of_completion(self):
        date_of_completion = self.cleaned_data['date_of_completion']
        today = datetime.date.today()
        if today > date_of_completion:
            raise ValidationError("Дата не должна быть меньше сегодняшней.")
        if date_of_completion.year - today.year > 2:
            raise ValidationError("К сожалению, мы не строим наши заказы на такой длиный период.")
        return date_of_completion