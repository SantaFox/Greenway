from functools import wraps

from django.shortcuts import render
from django.conf import settings
from django.template.response import TemplateResponse

from django_tables2 import RequestConfig

from products.models import Language
from .models import Account, Counterparty, Operation
from .tables import AccountsTable, CounterpartyTable, CustomerOrdersTable


def prepare_languages(view_func):
    """
    Decorator that language information
    """

    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):

        cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
        if cookie_lang in ('en', 'el', 'ru'):
            detail_lang = cookie_lang
        else:
            detail_lang = settings.LANGUAGE_CODE
        language = Language.objects.get(Code=detail_lang)
        languages = Language.objects.all().order_by('Code')

        response = view_func(request, *args, **kwargs)

        if type(response) == TemplateResponse:
            if not response.context_data:
                response.context_data = {}
            response.context_data['language'] = language
            response.context_data['languages'] = languages
            return response.render()
        else:
            raise TypeError(
                'Decorator \'@prepare_languages\' expects django.template.response.TemplateResponse as a view '
                'returned value')

    return _wrapped_view_func


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
