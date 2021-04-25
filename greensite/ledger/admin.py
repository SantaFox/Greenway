from django.contrib import admin

from .models import Account, Counterparty, SupplierOrder, SupplierOrderPosition, CustomerOrder, CustomerOrderPosition, \
    ItemSetBreakdown, ItemSetBreakdownPosition


class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('User', 'Name', 'Phone', 'City', 'IsSupplier', 'IsCustomer')
    # list_filter = ['Language', 'Product__Category', 'Product']
    list_editable = ['Name', 'Phone', 'City', 'IsSupplier', 'IsCustomer']
    ordering = ['User', 'Name']
    search_fields = ['Name']


class SupplierOrderPositionInline(admin.TabularInline):
    model = SupplierOrderPosition


class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'Counterparty', 'Amount', 'Currency', 'GFT', 'PV')
    list_filter = ['User', 'Counterparty']
    list_editable = ['DateOperation', 'Counterparty', 'Amount', 'Currency', 'GFT', 'PV']
    ordering = ['User', 'DateOperation', 'Counterparty__Name']
    inlines = [
        SupplierOrderPositionInline,
    ]


class CustomerOrderPositionInline(admin.TabularInline):
    model = CustomerOrderPosition


class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'Counterparty', 'Amount', 'Currency')
    list_filter = ['User', 'Counterparty']
    list_editable = ['DateOperation', 'Counterparty', 'Amount', 'Currency']
    ordering = ['User', 'DateOperation', 'Counterparty__Name']
    inlines = [
        CustomerOrderPositionInline,
    ]


class ItemSetBreakdownPositionInline(admin.TabularInline):
    model = ItemSetBreakdownPosition


class ItemSetBreakdownAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'Product', 'Quantity')
    list_filter = ['User', 'Product']
    list_editable = ['DateOperation', 'Product', 'Quantity']
    ordering = ['User', 'DateOperation', 'Product__SKU']
    inlines = [
        ItemSetBreakdownPositionInline,
    ]


admin.site.register(Account)
admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(SupplierOrder, SupplierOrderAdmin)
admin.site.register(CustomerOrder, CustomerOrderAdmin)
admin.site.register(ItemSetBreakdown, ItemSetBreakdownAdmin)
