from importlib import import_module

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView

from lyceum import settings

urlpatterns = [
    path('', include('homepage.urls')),
    path('about/', include('about.urls')),
    path('catalog/', include('catalog.urls')),
    path('admin/', admin.site.urls),
    path(
        'favicon.ico/',
        RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')),
    ),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    debug_toolbar = import_module('debug_toolbar.toolbar')
    urlpatterns += debug_toolbar.debug_toolbar_urls()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
