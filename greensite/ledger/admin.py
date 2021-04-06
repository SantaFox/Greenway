from django.contrib import admin

from .models import Account, Counterparty, Order, OrderPosition


class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('User', 'Name', 'Phone', 'IsSupplier', 'IsCustomer')
    # list_filter = ['Language', 'Product__Category', 'Product']
    list_editable = ['Name', 'Phone', 'IsSupplier', 'IsCustomer']
    ordering = ['User', 'Name']
    search_fields = ['Name']


admin.site.register(Account)
admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(Order)
admin.site.register(OrderPosition)