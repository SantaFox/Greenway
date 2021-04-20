from django.utils.safestring import mark_safe

from django_tables2 import A, BooleanColumn, LinkColumn, Table
from django_tables2.utils import AttributeDict

from .models import Account, Counterparty, Operation


class BootstrapBooleanColumn(BooleanColumn):
    def __init__(self, null=False, **kwargs):
        if null:
            kwargs["empty_values"] = ()
        super(BooleanColumn, self).__init__(**kwargs)

    def render(self, value):
        value = bool(value)
        html = "<i %s></i>"

        class_name = "bi bi-square"
        if value:
            class_name = "bi bi-check-square"
        attrs = {'class': class_name}

        attrs.update(self.attrs.get('span', {}))

        return mark_safe(html % (AttributeDict(attrs).as_html()))


class AccountsTable(Table):
    # WARNING!!! AUTHOR SAYS THAT LINKCOLUMN IS DEPRECATED!!! USE ANOTHER TYPE!!!

    # delete = LinkColumn('ledger:accounts', text=lambda record: record.id, args=[A('pk')], attrs={
    #     'a': {'class': 'btn'}
    # })

    class Meta:
        model = Account
        fields = ('Name', 'delete', )


class CounterpartyTable(Table):
    IsSupplier = BootstrapBooleanColumn()
    IsCustomer = BootstrapBooleanColumn()

    class Meta:
        model = Counterparty
        fields = ('Name', 'Phone', 'Email', 'Telegram', 'Memo', 'IsSupplier', 'IsCustomer', )
        # attrs = {'class': 'table-sm'}


class CustomerOrdersTable(Table):

    class Meta:
        model = Operation
        fields = ('DateOperation', 'Counterparty')
