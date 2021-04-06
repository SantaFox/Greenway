from django.contrib import admin

from .models import Account, Order, OrderPosition

admin.site.register(Account)
admin.site.register(Order)
admin.site.register(OrderPosition)