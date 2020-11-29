from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import TypePacking, Measurement, Packing
from additional_functions import get_verbose_of_field_from_class

# class EditTypePacking(forms.Form):
#     name = forms.CharField(label=get_verbose_of_field_from_class(TypePacking, 'name'))
#
#     def clean_name(self):
#         name = self.cleaned_data['name']
#         if name == "ф":
#             raise ValidationError("f")
#         return name
#


# class EditTypePacking(ModelForm):
#     class Meta:
#         model = TypePacking
#         fields = '__all__'
#         # fields = '__all__'
#         # fields = ['due_back', ]
#         # exclude
#
#     def clean_name(self):
#         name = self.cleaned_data['name']
#         if name == "ф":
#             raise ValidationError("f")
#         return name