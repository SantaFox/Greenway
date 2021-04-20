from django.shortcuts import render
from django.conf import settings

from django_tables2 import RequestConfig

from products.models import Language
from .models import Account, Counterparty
from .tables import AccountsTable, CounterpartyTable


def view_index(request):
    # Work with selected language
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)

    if cookie_lang in ('en', 'el', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = settings.LANGUAGE_CODE

    language = Language.objects.get(Code=detail_lang)
    languages = Language.objects.all().order_by('Code')

    response = render(request, 'ledger/index.html', {
        'language': language,
        'languages': languages,
    })

    return response


def table_counterparties(request):
    # Work with selected language
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)

    if cookie_lang in ('en', 'el', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = settings.LANGUAGE_CODE

    language = Language.objects.get(Code=detail_lang)
    languages = Language.objects.all().order_by('Code')

    table = CounterpartyTable(Counterparty.objects.all())
    RequestConfig(request).configure(table)

    return render (request, 'ledger/table_counterparties.html', {
        'language': language,
        'languages': languages,
        'table': table,
    })


def table_accounts(request):
    # Work with selected language
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)

    if cookie_lang in ('en', 'el', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = settings.LANGUAGE_CODE

    language = Language.objects.get(Code=detail_lang)
    languages = Language.objects.all().order_by('Code')

    table = AccountsTable(Account.objects.all())
    RequestConfig(request).configure(table)

    return render (request, 'ledger/table_accounts.html', {
        'language': language,
        'languages': languages,
        'table': table,
    })
