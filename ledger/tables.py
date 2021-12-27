from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_tables2 import A, Column, BooleanColumn, CheckBoxColumn, DateColumn, TemplateColumn, Table
from django_tables2.utils import AttributeDict

from .models import Account, Counterparty, CustomerOrder, CustomerOrderPosition, Payment


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


class InStockTable(Table):
    Category_Name = Column(verbose_name=_('Category'), accessor='product_category')
    Product_SKU = Column(verbose_name=_('SKU'), accessor='product_SKU')
    Product_Name = Column(verbose_name=_('Name'), accessor='product_name')
    In_Stock = Column(verbose_name=_('In Stock'), accessor='in_stock')

    class Meta:
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}
        row_attrs = {
            "class": lambda record: 'text-black-50' if record.get('in_stock') == 0 else ''
        }


class AccountsTable(Table):
    # id = PrimaryKeyCheckboxColumn()

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
        empty_text = _('There are no Accounts for this User')
        fields = ('Name', 'Actions',)
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}


class CounterpartyTable(Table):
    # id = PrimaryKeyCheckboxColumn()

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
        empty_text = _('There are no Counterparties for this User')
        fields = ('Name', 'Phone', 'City', 'Memo', 'IsSupplier', 'IsCustomer', 'Actions',)
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}


class CustomerOrdersTable(Table):
    DateOperation = DateColumn('d.m.Y')

    Amount = NumericColumn(attrs={
        "td": {"align": "right"}
    })

    Paid = NumericColumn(
        accessor=A('get_paid_amount'),
        attrs={"td": {"align": "right"}},
        verbose_name=_('Paid')
    )

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

    class Meta:
        model = CustomerOrder
        empty_text = _('There are no Customer Orders for this User')
        fields = ('DateOperation', 'Customer__Name', 'Amount', 'Currency', 'Paid', 'Memo', 'Actions',)
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}
        row_attrs = {
            "class": lambda record: 'text-black-50' if (record.Amount or 0) == (record.get_paid_amount or 0) else ''
        }


class CustomerOrderPositionsTable(Table):
    id = PrimaryKeyCheckboxColumn()

    ActualPrice = NumericColumn(
        accessor=A('get_actual_price'),
        attrs={"td": {"align": "right", 'class': 'text-black-50'}},
        verbose_name=_('Actual'),
    )

    Price = NumericColumn(attrs={
        "td": {"align": "right"}
    })

    Discount = NumericColumn(attrs={
        "td": {"align": "right"}
    })

    DateDelivered = DateColumn('d.m.Y')

    class Meta:
        model = CustomerOrderPosition
        empty_text = _('There are no Position for this Customer Order')
        fields = (
            'id', 'Product', 'ActualPrice', 'Price', 'Quantity', 'Currency', 'Discount', 'DiscountReason', 'Status',
            'DateDelivered')
        attrs = {"class": "table table-hover table-sm small", "thead": {"class": ""}}
        orderable = False


class CustomerOrderPaymentsTable(Table):
    id = PrimaryKeyCheckboxColumn()

    DateOperation = DateColumn('d.m.Y')

    Amount = NumericColumn(attrs={
        "td": {"align": "right"}
    })

    class Meta:
        model = Payment
        empty_text = _('There are no Payments for this Customer Order')
        fields = ('id', 'DateOperation', 'Account', 'Amount', 'Currency')
        attrs = {"class": "table table-hover table-sm small", "thead": {"class": ""}}
        orderable = False
