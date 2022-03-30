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
    attrs = {
        'td': {
#            'class': lambda value: 'text-danger' if value < 0 else '',
#            'align': 'right'
        }
    }

    def render(self, value):
        return '{:0,.2f}'.format(value)


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
    Product_SKU = Column(verbose_name=_('SKU'), accessor='product_SKU', linkify=("products:product", [A("product_SKU")]))
    Product_Name = Column(verbose_name=_('Name'), accessor='product_name')
    In_Stock = Column(verbose_name=_('In Stock'), accessor='in_stock')
    Receivable = Column(verbose_name=_('Receivable'), accessor='supp_not_delivered')
    Deliverable = Column(verbose_name=_('Deliverable'), accessor='cust_not_delivered')

    class Meta:
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}
        row_attrs = {
            "class": lambda record: 'text-black-50' if record.get('in_stock') == 0 and
                                                       record.get('supp_not_delivered') == 0 and
                                                       record.get('cust_not_delivered') == 0
                                                    else ''
        }


class FundsTable(Table):
    Account_Name = Column(verbose_name=_('Account'), accessor='account')
    Currency_Code = Column(verbose_name=_('Currency'), accessor='currency')
    Initial = NumericColumn(verbose_name=_('Initial'), accessor='initial')
    Debited = NumericColumn(verbose_name=_('Debited'), accessor='debited')
    Credited = NumericColumn(verbose_name=_('Credited'), accessor='credited')
    Final = NumericColumn(verbose_name=_('Final'), accessor='final')

    class Meta:
        attrs = {"class": "table table-hover table-sm", "thead": {"class": ""}}


class AccountsTable(Table):
    # id = PrimaryKeyCheckboxColumn()

    Actions = TemplateColumn(
        ('<a href="#editAccount" class="mr-2" data-toggle="modal" data-id="{{ value}}">'
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
        ('<a href="#editCounterparty" class="mr-2" data-toggle="modal" data-id="{{ value}}">'
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
        ('<a href="#editOrder" class="mr-2" data-toggle="modal" data-id="{{ value}}">'
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
    # id = PrimaryKeyCheckboxColumn()

    ProductName = TemplateColumn(
        '<p>{{ value }}</p>',
        accessor=A('get_product_name'),
        attrs={"td": {'class': 'original text-muted'},
               "th": {'class': 'original'}
               },
        verbose_name='',
    )

    Product__SKU = TemplateColumn(
        '#{{ value }}'
    )


    ActualPrice = NumericColumn(
        accessor=A('get_actual_price__Price'),
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

    Actions = TemplateColumn(
        ('<a href="#editPosition" class="mr-2" data-toggle="modal" data-id="{{ value}}">'
         '<i class="bi bi-pencil-square text-success mr-1"></i></a>'
         '<a href="#deleteModal" data-toggle="modal" data-id="{{ value }}">'
         '<i class="bi bi-trash text-danger mr-1"></i></a>'),
        accessor='id',
        orderable=False,
        verbose_name=_('Actions'),
    )

    class Meta:
        model = CustomerOrderPosition
        empty_text = _('There are no Position for this Customer Order')
        fields = (
            'ProductName', 'Product__SKU', 'ActualPrice', 'Price', 'Quantity', 'Discount',
            'DiscountReason', 'Status', 'DateDelivered')
        attrs = {"class": "table table-hover table-sm small", "thead": {"class": ""}}
        row_attrs = {"class": "has_original"}
        orderable = False


class CustomerOrderPaymentsTable(Table):
    # id = PrimaryKeyCheckboxColumn()

    DateOperation = DateColumn('d.m.Y')

    Amount = NumericColumn(attrs={
        "td": {"align": "right"}
    })

    Actions = TemplateColumn(
        ('<a href="#editPayment" class="mr-2" data-toggle="modal" data-id="{{ value}}">'
         '<i class="bi bi-pencil-square text-success mr-1"></i></a>'
         '<a href="#deleteModal" data-toggle="modal" data-id="{{ value }}">'
         '<i class="bi bi-trash text-danger mr-1"></i></a>'),
        accessor='id',
        orderable=False,
        verbose_name=_('Actions'),
    )

    class Meta:
        model = Payment
        empty_text = _('There are no Payments for this Customer Order')
        fields = ('DateOperation', 'TransactionType', 'Account__Name', 'Amount', 'Currency')
        attrs = {"class": "table table-hover table-sm small", "thead": {"class": ""}}
        orderable = False
