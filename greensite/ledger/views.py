from django.template.response import TemplateResponse

from django_tables2 import RequestConfig

from greensite.decorators import prepare_languages

from .models import Account, Counterparty, Operation
from .tables import AccountsTable, CounterpartyTable, CustomerOrdersTable


@prepare_languages
def view_index(request):
    return TemplateResponse(request, 'ledger/index.html')


@prepare_languages
def table_counterparties(request):
    table = CounterpartyTable(Counterparty.objects.filter(User=request.user))
    RequestConfig(request).configure(table)

    return TemplateResponse(request, 'ledger/table_counterparties.html', {
        'table': table,
    })


@prepare_languages
def table_accounts(request):
    table = AccountsTable(Account.objects.filter(User=request.user))
    RequestConfig(request).configure(table)

    return TemplateResponse(request, 'ledger/table_accounts.html', {
        'table': table,
    })


@prepare_languages
def table_customer_orders(request):
    table = CustomerOrdersTable(Operation.objects.filter(User=request.user, Type=1))
    RequestConfig(request).configure(table)

    return TemplateResponse(request, 'ledger/table_customer_orders.html', {
        'table': table,
    })
