from django.contrib import admin

from .models import Account, Counterparty, Operation, OperationPosition


class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('User', 'Name', 'Phone', 'IsSupplier', 'IsCustomer')
    # list_filter = ['Language', 'Product__Category', 'Product']
    list_editable = ['Name', 'Phone', 'IsSupplier', 'IsCustomer']
    ordering = ['User', 'Name']
    search_fields = ['Name']


class OperationPositionAdmin(admin.ModelAdmin):
    list_display = ('Operation', 'Product', 'Quantity', 'Price', 'Currency')
    list_filter = ['Operation']
    list_editable = ['Product', 'Quantity', 'Price', 'Currency']
    ordering = ['Operation__DateOperation', 'Operation']


admin.site.register(Account)
admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(Operation)
admin.site.register(OperationPosition, OperationPositionAdmin)