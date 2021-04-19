from django.shortcuts import render
from django.conf import settings

from products.models import Language


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
