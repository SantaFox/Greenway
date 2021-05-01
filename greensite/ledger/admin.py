from django.contrib import admin

from .models import Account, Counterparty, SupplierOrder, SupplierOrderPosition, CustomerOrder, CustomerOrderPosition, \
    ItemSetBreakdown, ItemSetBreakdownPosition, Payment, \
    Operation   # It is for customized


class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('User', 'Name', 'Phone', 'City', 'IsSupplier', 'IsCustomer')
    list_editable = ['Name', 'Phone', 'City', 'IsSupplier', 'IsCustomer']
    ordering = ['User', 'Name']
    search_fields = ['Name']


class SupplierOrderPositionInline(admin.TabularInline):
    model = SupplierOrderPosition


class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'Counterparty', 'GreenwayOrderNum', 'Amount', 'Currency', 'GFT', 'PV')
    list_filter = ['User', 'Counterparty']
    list_editable = ['GreenwayOrderNum', 'Amount', 'Currency', 'GFT', 'PV']
    ordering = ['User', 'DateOperation', 'Counterparty__Name']
    inlines = [
        SupplierOrderPositionInline,
    ]

    # It works for the form but not for the inline
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(SupplierOrderAdmin, self).get_form(request, obj, **kwargs)
    #     field = form.base_fields["Counterparty"]
    #     field.widget.can_add_related = False
    #     field.widget.can_change_related = False
    #     field.widget.can_delete_related = False
    #     return form


class CustomerOrderPositionInline(admin.TabularInline):
    model = CustomerOrderPosition


class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'Counterparty', 'Amount', 'Currency', 'DateDelivered')
    list_filter = ['User', 'Counterparty']
    list_editable = ['DateOperation', 'Counterparty', 'Amount', 'Currency', 'DateDelivered']
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


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'ParentOperation', 'TransactionType', 'Amount', 'Currency')
    list_filter = ['User', 'TransactionType']
    list_editable = ['DateOperation', 'ParentOperation', 'TransactionType', 'Amount', 'Currency']
    ordering = ['User', 'DateOperation']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ParentOperation":
            # TODO: Combine two querysets, CustomerOrders and SupplierOrders
            kwargs["queryset"] = Operation.objects.filter(Type__lte=2).order_by('DateOperation')
        return super(PaymentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Account)
admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(SupplierOrder, SupplierOrderAdmin)
admin.site.register(CustomerOrder, CustomerOrderAdmin)
admin.site.register(ItemSetBreakdown, ItemSetBreakdownAdmin)
admin.site.register(Payment, PaymentAdmin)
