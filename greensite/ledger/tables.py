from django.utils.safestring import mark_safe

import django_tables2 as tables
from django_tables2.utils import AttributeDict

from .models import Counterparty


class BootstrapBooleanColumn(tables.BooleanColumn):
    def __init__(self, null=False, **kwargs):
        if null:
            kwargs["empty_values"] = ()
        super(tables.BooleanColumn, self).__init__(**kwargs)

    def render(self, value):
        value = bool(value)
        html = "<i %s></i>"

        class_name = "bi bi-square"
        if value:
            class_name = "bi bi-check-square"
        attrs = {'class': class_name}

        attrs.update(self.attrs.get('span', {}))

        return mark_safe(html % (AttributeDict(attrs).as_html()))


class CounterpartyTable(tables.Table):
    IsSupplier = BootstrapBooleanColumn()
    IsCustomer = BootstrapBooleanColumn()

    class Meta:
        model = Counterparty
        fields = ('Name', 'Phone', 'Email', 'Telegram', 'Memo', 'IsSupplier', 'IsCustomer', )
        # attrs = {'class': 'table-sm'}