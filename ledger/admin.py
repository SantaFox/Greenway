from django.contrib import admin
from django.db.models import Q

from .models import Account, Counterparty, SupplierOrder, SupplierOrderPosition, CustomerOrder, CustomerOrderPosition, \
    ItemSetBreakdown, ItemSetBreakdownPosition, Payment, Transfer, \
    Operation   # It is for customized


class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('User', 'Name', 'Phone', 'City', 'IsSupplier', 'IsCustomer')
    list_editable = ['Name', 'Phone', 'City', 'IsSupplier', 'IsCustomer']
    ordering = ['User', 'Name']
    search_fields = ['Name']


class SupplierOrderPositionInline(admin.TabularInline):
    model = SupplierOrderPosition
    exclude = ('GFT',)


class SupplierOrderPaymentInLine(admin.TabularInline):
    model = Payment
    fk_name = 'ParentOperation'


class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'Counterparty', 'GreenwayOrderNum', 'Amount', 'Currency', 'DateDelivered', 'get_debt', 'Memo')
    list_filter = ['User', 'Counterparty']
    # list_editable = ['GreenwayOrderNum', 'Amount', 'Currency', 'PV']
    ordering = ['User', 'DateOperation', 'Counterparty__Name']
    inlines = [
        SupplierOrderPositionInline,
        SupplierOrderPaymentInLine
    ]

    @admin.display(description='Not Paid', empty_value='???')
    def get_debt(self, obj):
        return '{:0,.2f}'.format((obj.Amount or 0) - obj.get_paid_amount)

    class Media:
        css = {
            "all": ("admin/formatting.css",)
        }
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


class CustomerOrderPaymentInLine(admin.TabularInline):
    model = Payment
    fk_name = 'ParentOperation'


class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'Customer', 'Amount', 'Currency', 'DateDelivered', 'get_debt', 'Memo')
    list_filter = ['User', 'Customer']
    # list_editable = ['DateOperation', 'Customer', 'Amount', 'Currency', 'DateDelivered']
    ordering = ['User', 'DateOperation', 'Customer__Name']
    inlines = [
        CustomerOrderPositionInline,
        CustomerOrderPaymentInLine,
    ]

    @admin.display(description='Not Paid', empty_value='???')
    def get_debt(self, obj):
        return '{:0,.2f}'.format((obj.Amount or 0) - obj.get_paid_amount)

    class Media:
        css = {
            "all": ("admin/formatting.css",)
        }


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
    list_display = ('User', 'DateOperation', 'ParentOperation', 'TransactionType', 'Account', 'Amount', 'Currency')
    list_filter = ['User', 'TransactionType', 'Account']
    list_editable = ['DateOperation', 'Account', 'Amount', 'Currency']
    ordering = ['User', 'DateOperation']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ParentOperation":
            qry_CustomerOrders = CustomerOrder.objects.all()
            qry_SupplierOrders = SupplierOrder.objects.all()
            kwargs["queryset"] = Operation.objects \
                .filter(Q(id__in=qry_CustomerOrders) | Q(id__in=qry_SupplierOrders)) \
                .select_subclasses(CustomerOrder, SupplierOrder) \
                .order_by('DateOperation')
        return super(PaymentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class TransferAdmin(admin.ModelAdmin):
    list_display = ('User', 'DateOperation', 'DebitAccount', 'DebitAmount', 'DebitCurrency', 'CreditAccount', 'CreditAmount', 'CreditCurrency')
    list_filter = ['User', 'DebitAccount', 'CreditAccount']
    # list_editable = ['DateOperation', 'Account', 'Amount', 'Currency']
    ordering = ['User', 'DateOperation']


admin.site.register(Account)
admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(SupplierOrder, SupplierOrderAdmin)
admin.site.register(CustomerOrder, CustomerOrderAdmin)
admin.site.register(ItemSetBreakdown, ItemSetBreakdownAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transfer, TransferAdmin)