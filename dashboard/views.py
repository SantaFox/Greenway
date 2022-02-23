from django.template.response import TemplateResponse

from greensite.decorators import prepare_languages


@prepare_languages
def view_index(request):

    return TemplateResponse(request, 'dashboard/index.html', {
        'title': 'Dashboard',
    })

