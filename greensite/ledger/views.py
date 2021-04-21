from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from django_tables2 import RequestConfig

from greensite.decorators import prepare_languages

from .models import Account, Counterparty, Operation
from .tables import AccountsTable, CounterpartyTable, CustomerOrdersTable


@login_required
@prepare_languages
def view_index(request):
    return TemplateResponse(request, 'ledger/index.html')


@login_required
@permission_required('ledger.view_counterparty', raise_exception=True)
@prepare_languages
def table_counterparties(request):
    table = CounterpartyTable(Counterparty.objects.filter(User=request.user))
    RequestConfig(request).configure(table)

    return TemplateResponse(request, 'ledger/table_counterparties.html', {
        'table': table,
    })


@login_required
@permission_required('ledger.edit_account', raise_exception=True)
@prepare_languages
def edit_counterparty(request):
    return TemplateResponse(request, 'ledger/edit_counterparty.html', )


@login_required
@permission_required('ledger.delete_account', raise_exception=True)
@prepare_languages
def confirm_delete_counterparty(request):
    return TemplateResponse(request, 'ledger/delete_counterparty.html', )


@login_required
@permission_required('ledger.view_account', raise_exception=True)
@prepare_languages
def table_accounts(request):
    table = AccountsTable(Account.objects.filter(User=request.user))
    RequestConfig(request).configure(table)

    return TemplateResponse(request, 'ledger/table_accounts.html', {
        'table': table,
    })


@login_required
@permission_required('ledger.edit_account', raise_exception=True)
@prepare_languages
def edit_account(request, pk):
    account_instance = get_object_or_404(Account, pk=pk)
    return TemplateResponse(request, 'ledger/edit_account.html', {
        'account': account_instance,
    })


@login_required
@permission_required('ledger.delete_account', raise_exception=True)
@prepare_languages
def confirm_delete_account(request, pk):
    account_instance = get_object_or_404(Account, pk=pk)
    return TemplateResponse(request, 'ledger/delete_account.html', {
        'account': account_instance,
    })


@login_required
@permission_required('ledger.view_operation', raise_exception=True)
@prepare_languages
def table_customer_orders(request):
    table = CustomerOrdersTable(Operation.objects.filter(User=request.user, Type=1))
    RequestConfig(request).configure(table)

    return TemplateResponse(request, 'ledger/table_customer_orders.html', {
        'table': table,
    })
