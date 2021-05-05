from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.view_index, name='index'),
    path('products/', include('products.urls')),
    path('ledger/', include('ledger.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^markdownx/', include('markdownx.urls')),
    re_path('djga/', include('google_analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
