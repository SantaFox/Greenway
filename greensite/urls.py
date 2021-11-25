from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView


from . import views

urlpatterns = [
    path('', include('showcase.urls')),
    path('products/', include('products.urls')),
    path('ledger/', include('ledger.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^markdownx/', include('markdownx.urls')),
    # re_path('djga/', include('google_analytics.urls')),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # import debug_toolbar
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ]
