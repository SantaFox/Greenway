from django.utils.safestring import mark_safe
from django.urls import reverse

from django_tables2 import A, BooleanColumn, CheckBoxColumn, Column, DateColumn, EmailColumn, LinkColumn, Table
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


class PrimaryKeyCheckboxColumn(CheckBoxColumn):

    @property
    def header(self):
        # default = {"type": "checkbox"}
        # general = self.attrs.get("input")
        # specific = self.attrs.get("th__input")
        # attrs = AttributeDict(default, **(specific or general or {}))
        # return mark_safe("<input %s/>" % attrs.as_html())
        html = (f'<div class="custom-control custom-checkbox text-center">'
                f'<input type="checkbox" class="custom-control-input" id="selectAll">'
                f'<label class="custom-control-label" for="selectAll"></label>'
                f'</div>'
                )
        return mark_safe(html)

    def render(self, value):
        html = (f'<div class="custom-control custom-checkbox text-center">'
                f'<input type="checkbox" class="custom-control-input" value="{value}" id="tableCheck{value}">'
                f'<label class="custom-control-label" for="tableCheck{value}"></label>'
                f'</div>'
                )
        return mark_safe(html)


class AccountsTable(Table):
    id = PrimaryKeyCheckboxColumn()

    actions = Column(
        accessor='pk',
        orderable=False,
    )

    def render_actions(self, value):
        url_edit = reverse('ledger:edit_account', args=[value])
        url_delete = reverse('ledger:delete_account', args=[value])
        html = (f'<a href="#editAccountModal" class="mr-2" data-toggle="modal" data-id="{value}"><i class="bi bi-pencil-square text-success mr-1"></i>Edit</a>'
                f'<a href="#deleteAccountModal" data-toggle="modal" data-id="{value}"><i class="bi bi-trash text-danger mr-1"></i>Delete</a>'
                )
        return mark_safe(html)

    class Meta:
        model = Account
        empty_text = 'There are no accounts on this user'
        fields = ('id', 'Name', 'actions',)
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}


class CounterpartyTable(Table):
    Email = EmailColumn()
    IsSupplier = BootstrapBooleanColumn()
    IsCustomer = BootstrapBooleanColumn()
    Action = Column()

    class Meta:
        model = Counterparty
        fields = ('Name', 'Phone', 'Email', 'Telegram', 'Memo', 'IsSupplier', 'IsCustomer', 'Action',)
        # attrs = {'class': 'table-sm'}


class CustomerOrdersTable(Table):
    DateOperation = DateColumn()

    class Meta:
        model = Operation
        fields = ('DateOperation', 'Counterparty')
