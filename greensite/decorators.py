from functools import wraps

from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from products.models import Language, Category

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

        # nice trick
        request.language_instance = language

        nav_categories = Category.objects.all().order_by('Order')

        response = view_func(request, *args, **kwargs)

        if type(response) == TemplateResponse:
            if not response.context_data:
                response.context_data = {}
            response.context_data['language'] = language
            response.context_data['languages'] = languages
            response.context_data['nav_categories'] = nav_categories
            return response.render()
        elif type(response) == HttpResponseRedirect:
            # do nothing - it is just a redirect
            return response
        else:
            raise TypeError(
                'Decorator \'@prepare_languages\' expects django.template.response.TemplateResponse as a view '
                'returned value')

    return _wrapped_view_func
