from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.template.response import TemplateResponse
from django.forms.models import model_to_dict

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


def account_action(request):
    if request.is_ajax():
        if request.method == 'GET':
            request_id = request.GET.get('id')
            account_instance = get_object_or_404(Account, id=request_id)
            account_dict = model_to_dict(account_instance, fields=['id', 'Name',])
            return JsonResponse(account_dict)
        elif request.method == 'POST':
            request_id = request.POST.get('account_id')
            account_instance = get_object_or_404(Account, id=request_id)
            account_instance.Name = request.POST.get('account_name')
            # if account_instance.is_valid() and account_instance.has_changed():
            account_instance.save()
            return JsonResponse({'status': 'success'})
        else:
            raise Http404
    else:
        raise Http404



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
