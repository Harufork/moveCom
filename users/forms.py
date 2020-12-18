from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class DateTypeInput(forms.DateInput):
    input_type = 'date'


class TimeTypeInput(forms.TimeInput):
    input_type = 'time'


class PhoneTypeInput(forms.TextInput):
    input_type = 'tel'


class SignUpForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\+\d\(\d{3}\)\d{3}\-\d{2}\-\d{2}$',
                                 message="Введите номер телефона в формате: '+7 (999) 999-99-99'.")
    patronymic = forms.CharField(max_length=255, label="Отчество")
    birth_date = forms.DateField(label="Дата рождения",
                                 widget=DateTypeInput())
    phone_number = forms.CharField(validators=[phone_regex], max_length=18,
                               label="Номер телефона",
                               widget=PhoneTypeInput(attrs=
                                                     {'class': "mask-phone",
                                                      'pattern': "[+]\d[(]\d{3}[)]\d{3}[-]\d{2}[-]\d{2}"
                                                      }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'birth_date', 'password1', 'password2',)
