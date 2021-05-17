from django.conf import settings

# TODO: I like an idea to translate languages by context processors, not by decorators


def debug_context(request):
    debug_flag = settings.DEBUG
    return{"debug_flag": debug_flag}
