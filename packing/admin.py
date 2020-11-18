from django.contrib import admin
from .models import TypePacking, UnitOfMeasurement, Packing

admin.site.register(TypePacking)
admin.site.register(UnitOfMeasurement)
admin.site.register(Packing)