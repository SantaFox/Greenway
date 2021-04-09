from django.shortcuts import render

from products.views import Language


def view_index(request):
    # Work with selected language
    if not request.COOKIES.get('lang'):
        cookie_lang = ''
    else:
        cookie_lang = request.COOKIES.get('lang')

    if cookie_lang in ('eng', 'gr', 'ru'):
        detail_lang = cookie_lang
    else:
        detail_lang = 'eng'

    language = Language.objects.get(Code=detail_lang)
    languages = Language.objects.all().order_by('Code')

    response = render(request, 'greensite/index.html', {
        'language': language,
        'languages': languages,
    })

    if not request.COOKIES.get('lang'):
        response.set_cookie('lang', detail_lang)

    return response
