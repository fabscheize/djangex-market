from importlib import import_module

from django.contrib import admin
from django.urls import include, path
from lyceum import settings


urlpatterns = [
    path('', include('homepage.urls')),
    path('about/', include('about.urls')),
    path('catalog/', include('catalog.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    debug_toolbar = import_module('debug_toolbar.toolbar')
    urlpatterns += debug_toolbar.debug_toolbar_urls()
