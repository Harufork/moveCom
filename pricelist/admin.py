from django.contrib import admin
from .models import PriceRole, PriceModeTransport, \
    PriceModeTDistance, PricePacking


admin.site.register(PriceRole)
admin.site.register(PriceModeTransport)
admin.site.register(PriceModeTDistance)
admin.site.register(PricePacking)