from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_tables2 import Column, BooleanColumn, CheckBoxColumn, DateColumn, TemplateColumn, Table
from django_tables2.utils import AttributeDict

from .models import Account, Counterparty, CustomerOrder


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


class NumericColumn(Column):

    def render(self, value):
        return '{:0.2f}'.format(value)


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

    Actions = TemplateColumn(
        ('<a href="#editModal" class="mr-2" data-toggle="modal" data-id="{{ value}}">'
         '<i class="bi bi-pencil-square text-success mr-1"></i>Edit</a>'
         '<a href="#deleteModal" data-toggle="modal" data-id="{{ value }}">'
         '<i class="bi bi-trash text-danger mr-1"></i>Delete</a>'),
        accessor='id',
        orderable=False,
        verbose_name=_('Actions'),
    )

    class Meta:
        model = Account
        empty_text = 'There are no Accounts for this User'
        fields = ('id', 'Name', 'Actions',)
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}


class CounterpartyTable(Table):
    id = PrimaryKeyCheckboxColumn()

    Memo = TemplateColumn('<span data-toggle="tooltip" title="{{ value }}">{{ value|truncatechars:20 }}</span>',
                          empty_values=(None, ''),
                          orderable=False)

    IsSupplier = BootstrapBooleanColumn()
    IsCustomer = BootstrapBooleanColumn()

    Actions = TemplateColumn(
        ('<a href="#editModal" class="mr-2" data-toggle="modal" data-id="{{ value}}">'
         '<i class="bi bi-pencil-square text-success mr-1"></i>Edit</a>'
         '<a href="#deleteModal" data-toggle="modal" data-id="{{ value }}">'
         '<i class="bi bi-trash text-danger mr-1"></i>Delete</a>'),
        accessor='id',
        orderable=False,
        verbose_name=_('Actions'),
    )

    class Meta:
        model = Counterparty
        empty_text = 'There are no Counterparties for this User'
        fields = ('id', 'Name', 'Phone', 'City', 'Memo', 'IsSupplier', 'IsCustomer', 'Actions',)
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}


class CustomerOrdersTable(Table):
    id = PrimaryKeyCheckboxColumn()

    Amount = NumericColumn(attrs={
        "td": {"align": "right"}
    })

    Memo = TemplateColumn('<span data-toggle="tooltip" title="{{ value }}">{{ value|truncatechars:20 }}</span>',
                          empty_values=(None, ''),
                          orderable=False)

    Actions = TemplateColumn(
        ('<a href="#editModal" class="mr-2" data-toggle="modal" data-id="{{ value}}">'
         '<i class="bi bi-pencil-square text-success mr-1"></i>Edit</a>'
         '<a href="#deleteModal" data-toggle="modal" data-id="{{ value }}">'
         '<i class="bi bi-trash text-danger mr-1"></i>Delete</a>'),
        accessor='id',
        orderable=False,
        verbose_name=_('Actions'),
    )

    DateOperation = DateColumn()

    class Meta:
        model = CustomerOrder
        empty_text = 'There are no Customer Orders for this User'
        fields = ('id', 'DateOperation', 'Counterparty__Name', 'Amount', 'Currency', 'Paid', 'Memo', 'Actions',)
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}
