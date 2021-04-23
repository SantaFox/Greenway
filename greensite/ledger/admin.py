from django.contrib import admin

from .models import Account, Counterparty, Operation, OperationPosition, OperationAtom


class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('User', 'Name', 'Phone', 'City', 'IsSupplier', 'IsCustomer')
    # list_filter = ['Language', 'Product__Category', 'Product']
    list_editable = ['Name', 'Phone', 'City', 'IsSupplier', 'IsCustomer']
    ordering = ['User', 'Name']
    search_fields = ['Name']


class OperationPositionInline(admin.TabularInline):
    model = OperationPosition


class OperationAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'Type', 'Counterparty')
    list_filter = ['User', 'Type', 'Counterparty']
    ordering = ['User', 'DateOperation', 'Type', 'Counterparty__Name']
    inlines = [
        OperationPositionInline,
    ]


class OperationPositionAdmin(admin.ModelAdmin):
    list_display = ('Operation', 'Product', 'Quantity', 'Price', 'Currency')
    list_filter = ['Operation']
    list_editable = ['Product', 'Quantity', 'Price', 'Currency']
    ordering = ['Operation__DateOperation', 'Operation']


admin.site.register(Account)
admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(OperationPosition, OperationPositionAdmin)
admin.site.register(OperationAtom)
