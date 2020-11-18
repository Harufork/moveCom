from django.contrib import admin
from .models import PriceListRole, PriceListModeTransport, \
    PriceListModeTDistance, PriceListPacking


admin.site.register(PriceListRole)
admin.site.register(PriceListModeTransport)
admin.site.register(PriceListModeTDistance)
admin.site.register(PriceListPacking)