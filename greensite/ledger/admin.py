from django.contrib import admin

from .models import Account, Counterparty, Order, OrderPosition

admin.site.register(Account)
admin.site.register(Counterparty)
admin.site.register(Order)
admin.site.register(OrderPosition)